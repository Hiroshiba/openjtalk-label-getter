import argparse
import re
from pathlib import Path
from subprocess import PIPE, Popen


def openjtalk_label_getter(
        text: str,
        openjtalk_command: str,
        dict_path: Path,
        htsvoice_path: Path,
        output_wave_path: Path,
        output_log_path: Path,
):
    p_text = Popen(['echo', text], stdout=PIPE)
    p_openjtalk = Popen(
        [
            openjtalk_command,
            '-x', dict_path,
            '-m', htsvoice_path,
            '-ow', output_wave_path,
            '-ot', output_log_path,
        ],
        stdin=p_text.stdout,
    )
    p_openjtalk.wait()

    log = output_log_path.read_text()
    labels = re.split(r'\[.+\]', log)[2].splitlines()

    for label in filter(lambda x: len(x) > 0, labels):
        match = re.fullmatch(r'(\d+) (\d+) .+\^.+-(.+)\+.+=.+/A.+/B.+/C.+/D.+/E.+/F.+/G.+/H.+/I.+/J.+/K.+', label)
        start, end, phoneme = match.groups()
        print(f'{int(start) / 10 / 1000 / 1000:.4f} {int(end) / 10 / 1000 / 1000:.4f} {phoneme}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    parser.add_argument('--openjtalk_command',
                        default='open_jtalk')
    parser.add_argument('--dict_path', type=Path,
                        default=Path('/var/lib/mecab/dic/open-jtalk/naist-jdic'))
    parser.add_argument('--htsvoice_path', type=Path,
                        default=Path('/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'))
    parser.add_argument('--output_wave_path', type=Path,
                        default=Path('/tmp/tmp_openjtalk_label_getter.wav'))
    parser.add_argument('--output_log_path', type=Path,
                        default=Path('/tmp/tmp_openjtalk_label_getter.txt'))
    openjtalk_label_getter(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
