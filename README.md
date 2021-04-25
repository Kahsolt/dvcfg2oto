# dvcfg2oto

    A python commandline script for DeepVocal dvcfg config to UTAU oto config conversion.

## Usage

- check everything in `config.py`
- run `python3 dvcfg2oto.py <path_to_dvcfg>` such like
  - `python3 dvcfg2oto.py D:\VoiceDB\mylib\wav`
  - `python3 dvcfg2oto.py D:\VoiceDB\mylib\wav\voice.dvcfg`
  - `python3 dvcfg2oto.py "D:\VoiceDB\my lib\wav\voice.dvcfg_bak"`

## Principles & Conversion Model

```ini
[voice.dvcfg]
  "C5->E" : {
    "wavName" : "N_E.wav",
    "pitch" : "C5",
    "srcType" : "CV",                      # ["CV", "VX"]
    "symbol" : "E",
    "connectPoint" : 0.05999999865889549,  # in sec, %.17f
    "preutterance" : 0.1112938486039639,
    "vowelStart" : 0.1812273822724819,
    "vowelEnd" : 0.4076417051255703,
    "tailPoint" : 0.4626417037844659,
    "startTime" : 0.9026607908308506,
    "endTime" : 1.370302494615316,
    "updateTime" : "2020-08-06 08:33:34",  # str(datetime.now())[:-7]
  }
  NOTE:
    CP = startTime + connectPoint
    PP = startTime + preutterance
    VSP = startTime + vowelStart
    VEP = startTime + vowelEnd
    SP = startTime + connectPoint
    EP = startTime + tailPoint
    endTime = startTime + tailPoint + [0.005 for CV / 0.05 for VX]
    connectPoint = HEADING_TAILING_DEADZONE = 0.06

[oto.ini]
  あ.wav=あ,6,52,69,0,0                    # in mili-sec
  <wavName>=<symbol>,<offset>,<consonant>,<blank>,<preutterance>,<overlap>
                      起始空白  非拉伸时长 -结束空白 节奏点/元音开头  VC重叠
                        紫色     粉红色      紫色  ;      红线         绿线
                      *剩下的部分即为白色; 两条线应该在粉红色区域内，绿左红右
  NOTE:
    offset、consonant、blank是区块的时长
    overlap、preutterance是相对于offset的坐标偏移量

[dvcfg2oto换算模型]
   offset = CP = (startTime + connectPoint) * 1000
   consonant = VSP - CP = (vowelStart - connectPoint) * 1000
   blank = wav_dur - VEP = (wav_dur - startTime - vowelEnd) * 1000
   preutterance = PP - CP = (preutterance - connectPoint) * 1000
   overlap = OVERLAP_FACTOR * (PP - CP)
```

#### reference

For reverse conversion see: [oto2dvcfg](https://github.com/justln1113/oto2dvcfg)

----

by Armit
2021/04/24 
