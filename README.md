# OpenJTalk label getter
OpenJTalkで音声合成する際に得られるラベルを取得します。

## Requirements
```bash
sudo apt-get install -y open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001
```

## Install
```bash
pip install git+https://github.com/Hiroshiba/openjtalk-label-getter
```

## Usage
```bash
$ openjtalk_label_getter こんにちは
0.0000 0.3100 sil
0.3100 0.4350 k
0.4350 0.5150 o
0.5150 0.5750 N
0.5750 0.6350 n
0.6350 0.6950 i
0.6950 0.7850 ch
0.7850 0.8300 i
0.8300 0.9650 w
0.9650 1.0800 a
1.0800 1.6050 sil
```

## LICENSE
[MIT License](./LICENSE)
