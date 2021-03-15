import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory
from typing import List, Optional


class OutputType(str, Enum):
    phoneme = "phoneme"
    full_context_label = "full_context_label"
    yomi = "yomi"


@dataclass
class Label:
    start: Optional[float]
    end: Optional[float]
    label: str


def openjtalk_label_getter(
    text: str,
    openjtalk_command: str,
    dict_path: Path,
    htsvoice_path: Path,
    output_wave_path: Optional[Path],
    output_log_path: Optional[Path],
    output_type: OutputType,
    without_span: bool,
):
    p_text = Popen(["echo", text], stdout=PIPE)
    with TemporaryDirectory() as d:
        tmp_dir = Path(d)

        tmp_output_wave_path = tmp_dir.joinpath("output.wav")
        tmp_output_log_path = tmp_dir.joinpath("output.txt")
        subprocess.run(
            [
                openjtalk_command,
                "-x",
                dict_path,
                "-m",
                htsvoice_path,
                "-ow",
                tmp_output_wave_path,
                "-ot",
                tmp_output_log_path,
            ],
            stdin=p_text.stdout,
        )

        log = tmp_output_log_path.read_text()

        if output_wave_path is not None:
            shutil.move(str(tmp_output_wave_path), str(output_wave_path))
        if output_log_path is not None:
            shutil.move(str(tmp_output_log_path), str(output_log_path))

    outputs: List[Label] = []

    if output_type in [OutputType.phoneme, OutputType.full_context_label]:
        labels = re.split(r"\[.+\]", log)[2].splitlines()
        for label in filter(lambda x: len(x) > 0, labels):
            match = re.fullmatch(
                r"(\d+) (\d+) (.+\^.+-(.+)\+.+=.+/A.+/B.+/C.+/D.+/E.+/F.+/G.+/H.+/I.+/J.+/K.+)",
                label,
            )
            assert match is not None

            start, end, full_context_label, phoneme = match.groups()

            outputs.append(
                Label(
                    start=int(start) / 10 / 1000 / 1000 if not without_span else None,
                    end=int(end) / 10 / 1000 / 1000 if not without_span else None,
                    label=(
                        phoneme
                        if output_type == OutputType.phoneme
                        else full_context_label
                    ),
                )
            )

    elif output_type == OutputType.yomi:
        assert without_span

        labels = re.split(r"\[.+\]", log)[1].splitlines()

        for label in filter(lambda x: len(x) > 0, labels):
            match = re.fullmatch(
                r".+,.+,.+,.+,.+,.+,.+,.+,.+,(.+),.+,.+,.+",
                label,
            )
            assert match is not None

            (yomi,) = match.groups()

            for s in yomi:
                outputs.append(Label(start=None, end=None, label=s))

    else:
        raise ValueError(output_type)

    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    parser.add_argument("--openjtalk_command", default="open_jtalk")
    parser.add_argument(
        "--dict_path",
        type=Path,
        default=Path("/var/lib/mecab/dic/open-jtalk/naist-jdic"),
    )
    parser.add_argument(
        "--htsvoice_path",
        type=Path,
        default=Path(
            "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
        ),
    )
    parser.add_argument("--output_wave_path", type=Path)
    parser.add_argument("--output_log_path", type=Path)
    parser.add_argument(
        "--output_type",
        type=OutputType,
        default=OutputType.phoneme,
        choices=[t.value for t in OutputType],
    )
    parser.add_argument("--without_span", action="store_true")
    outputs = openjtalk_label_getter(**vars(parser.parse_args()))

    for p in outputs:
        if p.start is not None:
            print(f"{p.start:.4f} {p.end:.4f} {p.label}")
        else:
            print(f"{p.label}")


if __name__ == "__main__":
    main()
