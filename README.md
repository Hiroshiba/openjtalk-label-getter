# OpenJTalk label getter
OpenJTalkで音声合成する際に得られるラベルを取得します。
音素ラベルとフルコンテキストラベルに対応しています。

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
# 音素ラベル
openjtalk_label_getter こんにちは --output_type phoneme
"""
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
"""

# フルコンテキストラベル
python openjtalk_label_getter/__init__.py こんにちは --output_type full_context_label
"""
0.0000 0.3100 xx^xx-sil+k=o/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:5_5%0_xx-xx/H:xx_xx/I:xx-xx@xx+xx&xx-xx|xx+xx/J:1_5/K:1+1-5
0.3100 0.4350 xx^sil-k+o=N/A:-4+1+5/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
0.4350 0.5150 sil^k-o+N=n/A:-4+1+5/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
0.5150 0.5750 k^o-N+n=i/A:-3+2+4/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
0.5750 0.6350 o^N-n+i=ch/A:-2+3+3/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
0.6350 0.6950 N^n-i+ch=i/A:-2+3+3/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
0.6950 0.7850 n^i-ch+i=w/A:-1+4+2/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
0.7850 0.8300 i^ch-i+w=a/A:-1+4+2/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
0.8300 0.9650 ch^i-w+a=sil/A:0+5+1/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
0.9650 1.0800 i^w-a+sil=xx/A:0+5+1/B:xx-xx_xx/C:09_xx+xx/D:xx+xx_xx/E:xx_xx!xx_xx-xx/F:5_5#0_xx@1_1|1_5/G:xx_xx%xx_xx-xx/H:xx_xx/I:1-5@1+1&1-1|1+5/J:xx_xx/K:1+1-5
1.0800 1.6050 w^a-sil+xx=xx/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:xx+xx_xx/E:5_5!0_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:xx_xx%xx_xx-xx/H:1_5/I:xx-xx@xx+xx&xx-xx|xx+xx/J:xx_xx/K:1+1-5
"""
```

## LICENSE
[MIT License](./LICENSE)
