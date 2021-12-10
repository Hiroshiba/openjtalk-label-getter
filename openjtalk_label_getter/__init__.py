import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory
from typing import Dict, List, Optional, Union


class OutputType(str, Enum):
    phoneme = "phoneme"
    full_context_label = "full_context_label"
    yomi = "yomi"


@dataclass
class FullContextLabel:
    contexts: Dict[str, str]

    @classmethod
    def from_label(cls, label: str):
        contexts = re.search(
            r"^(?P<p1>.+?)\^(?P<p2>.+?)\-(?P<p3>.+?)\+(?P<p4>.+?)\=(?P<p5>.+?)"
            r"/A\:(?P<a1>.+?)\+(?P<a2>.+?)\+(?P<a3>.+?)"
            r"/B\:(?P<b1>.+?)\-(?P<b2>.+?)\_(?P<b3>.+?)"
            r"/C\:(?P<c1>.+?)\_(?P<c2>.+?)\+(?P<c3>.+?)"
            r"/D\:(?P<d1>.+?)\+(?P<d2>.+?)\_(?P<d3>.+?)"
            r"/E\:(?P<e1>.+?)\_(?P<e2>.+?)\!(?P<e3>.+?)\_(?P<e4>.+?)\-(?P<e5>.+?)"
            r"/F\:(?P<f1>.+?)\_(?P<f2>.+?)\#(?P<f3>.+?)\_(?P<f4>.+?)\@(?P<f5>.+?)\_(?P<f6>.+?)\|(?P<f7>.+?)\_(?P<f8>.+?)"  # noqa
            r"/G\:(?P<g1>.+?)\_(?P<g2>.+?)\%(?P<g3>.+?)\_(?P<g4>.+?)\_(?P<g5>.+?)"
            r"/H\:(?P<h1>.+?)\_(?P<h2>.+?)"
            r"/I\:(?P<i1>.+?)\-(?P<i2>.+?)\@(?P<i3>.+?)\+(?P<i4>.+?)\&(?P<i5>.+?)\-(?P<i6>.+?)\|(?P<i7>.+?)\+(?P<i8>.+?)"  # noqa
            r"/J\:(?P<j1>.+?)\_(?P<j2>.+?)"
            r"/K\:(?P<k1>.+?)\+(?P<k2>.+?)\-(?P<k3>.+?)$",
            label,
        ).groupdict()
        return cls(contexts=contexts)

    @property
    def phoneme(self):
        return self.contexts["p3"]

    @property
    def label(self):
        return (
            "{p1}^{p2}-{p3}+{p4}={p5}"
            "/A:{a1}+{a2}+{a3}"
            "/B:{b1}-{b2}_{b3}"
            "/C:{c1}_{c2}+{c3}"
            "/D:{d1}+{d2}_{d3}"
            "/E:{e1}_{e2}!{e3}_{e4}-{e5}"
            "/F:{f1}_{f2}#{f3}_{f4}@{f5}_{f6}|{f7}_{f8}"
            "/G:{g1}_{g2}%{g3}_{g4}_{g5}"
            "/H:{h1}_{h2}"
            "/I:{i1}-{i2}@{i3}+{i4}&{i5}-{i6}|{i7}+{i8}"
            "/J:{j1}_{j2}"
            "/K:{k1}+{k2}-{k3}"
        ).format(**self.contexts)

    def __repr__(self):
        return f"<FullContextLabel phoneme='{self.phoneme}'>"

    def __str__(self) -> str:
        return self.label


@dataclass
class Label:
    start: Optional[float]
    end: Optional[float]
    label: Union[str, FullContextLabel]


def openjtalk_label_getter(
    text: str,
    openjtalk_command="open_jtalk",
    dict_path=Path("/var/lib/mecab/dic/open-jtalk/naist-jdic"),
    htsvoice_path=Path(
        "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
    ),
    output_wave_path: Optional[Path] = None,
    output_log_path: Optional[Path] = None,
    output_type=OutputType.phoneme,
    without_span=False,
    raise_error_with_worning=False,
):
    p_text = Popen(["echo", text], stdout=PIPE)
    with TemporaryDirectory() as d:
        tmp_dir = Path(d)

        tmp_output_wave_path = tmp_dir.joinpath("output.wav")
        tmp_output_log_path = tmp_dir.joinpath("output.txt")
        p = subprocess.run(
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
            stderr=subprocess.PIPE,
            text=True,
        )
        if "ERROR" in p.stderr.upper():
            raise ValueError(p.stderr)
        if raise_error_with_worning and "WARNING" in p.stderr.upper():
            raise ValueError(p.stderr)

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

            start, end, context, phoneme = match.groups()
            full_context_label = FullContextLabel.from_label(context)

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
    parser.add_argument("--raise_error_with_worning", action="store_true")
    outputs = openjtalk_label_getter(**vars(parser.parse_args()))

    for p in outputs:
        if p.start is not None:
            print(f"{p.start:.4f} {p.end:.4f} {p.label}")
        else:
            print(f"{p.label}")


if __name__ == "__main__":
    main()
