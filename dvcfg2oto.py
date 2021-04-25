#!/usr/bin/env python3
# Author: Armit
# Create Time: 2021/04/24 

import sys
import json
import wave
import shutil
from pathlib import Path

import config as hp

#
# [voice.dvcfg]
#   "C5->E" : {
#     "wavName" : "N_E.wav",
#     "pitch" : "C5",
#     "srcType" : "CV",                      # ["CV", "VX"]
#     "symbol" : "E",
#     "connectPoint" : 0.05999999865889549,  # in sec, %.17f
#     "preutterance" : 0.1112938486039639,
#     "vowelStart" : 0.1812273822724819,
#     "vowelEnd" : 0.4076417051255703,
#     "tailPoint" : 0.4626417037844659,
#     "startTime" : 0.9026607908308506,
#     "endTime" : 1.370302494615316,
#     "updateTime" : "2020-08-06 08:33:34",  # str(datetime.now())[:-7]
#   }
#   NOTE:
#     CP = startTime + connectPoint
#     PP = startTime + preutterance
#     VSP = startTime + vowelStart
#     VEP = startTime + vowelEnd
#     SP = startTime + connectPoint
#     EP = startTime + tailPoint
#     endTime = startTime + tailPoint + [0.005 for CV / 0.05 for VX]
#     connectPoint = HEADING_TAILING_DEADZONE = 0.06
#
# [oto.ini]
#   あ.wav=あ,6,52,69,0,0                    # in mili-sec
#   <wavName>=<symbol>,<offset>,<consonant>,<blank>,<preutterance>,<overlap>
#                       起始空白  非拉伸时长 -结束空白 节奏点/元音开头  VC重叠
#                         紫色     粉红色      紫色  ;      红线         绿线
#                       *剩下的部分即为白色; 两条线应该在粉红色区域内，绿左红右
#   NOTE:
#     offset、consonant、blank是区块的时长
#     overlap、preutterance是相对于offset的坐标偏移量
#
# [dvcfg2oto换算模型]
#    offset = CP = (startTime + connectPoint) * 1000
#    consonant = VSP - CP = (vowelStart - connectPoint) * 1000
#    blank = wav_dur - VEP = (wav_dur - startTime - vowelEnd) * 1000
#    preutterance = PP - CP = (preutterance - connectPoint) * 1000
#    overlap = OVERLAP_FACTOR * (PP - CP)
#


# Utility
def open(fp, rw='r', **kwargs):
  from builtins import open as _open
  return _open(fp, rw, encoding=hp.FILE_ENCODING, **kwargs)

def get_duration(fp) -> float:
  with wave.open(fp) as wav:
    return wav.getnframes() / wav.getframerate()

def sec2mili(sec) -> int:
  return int(round(sec * 1000))


# Functionality
def dvcfg2oto(fp):
  # load dvcfg
  fp = Path(fp)
  if fp.is_dir:
    fp = fp / hp.DVCFG_FILENAME
  with open(fp) as fh:
    dvcfg = json.load(fh)
  print(f'[dvcfg] read {len(dvcfg)} config items')

  # parse dvcfg to oto
  dur = {}
  oto = []
  for c in dvcfg.values():
    if c['srcType'] != 'CV': continue
    
    symbol = c['symbol']
    wavName = c['wavName']
    if wavName not in dur:
      try:
        dur[wavName] = get_duration(str(fp.parent / wavName))
      except Exception as e:
        print(f'[Error] cannot load {wavName} for {symbol!r}')
        print(f'  >> {e!r}')
        continue
    
    offset = sec2mili(c['startTime'] + c['connectPoint'])
    consonant = sec2mili(c['vowelStart'] - c['connectPoint'])
    blank = sec2mili(dur[wavName] - c['startTime'] - c['vowelEnd'])
    preutterance = sec2mili(c['preutterance'] - c['connectPoint'])
    overlap = int(hp.OVERLAP_FACTOR * preutterance)
    oto.append([wavName, symbol, offset, consonant, blank, preutterance, overlap])
  
  # write oto
  oto_fp = fp.parent / hp.OTO_FILENAME
  if oto_fp.exists and hp.OTO_MAKE_BACKUP:
    oto_bak_fp = Path(str(oto_fp) + '_bak')
    shutil.move(oto_fp, oto_bak_fp)
    print(f'[oto-bak] move {oto_fp!s} to {oto_bak_fp!s}')
  with open(oto_fp, 'w') as fh:
    for o in sorted(oto):
      fh.write(f'{o[0]}={o[1]},{o[2]},{o[3]},{o[4]},{o[5]},{o[6]}\n')
  print(f'[oto] write {len(oto)} config items')
  
  print(f'[Done] saved to {(fp.parent / hp.OTO_FILENAME)!s}')

# Main
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <path_to_dvcfg>')
    exit(-1)
  
  dvcfg2oto(sys.argv[1])
