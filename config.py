#!/usr/bin/env python3
# Author: Armit
# Create Time: 2021/04/25 

########
# File

FILE_ENCODING = 'utf-8'
DVCFG_FILENAME = 'voice.dvcfg'
OTO_FILENAME = 'oto.ini'
OTO_MAKE_BACKUP = True


############
# Mechanism

# if 'const', set `overlap=OVERLAP_FACTOR*(PP-CP)` for all symbols
# if 'auto',  set `overlap=0` for symbols begin with UNVOICED_CONSONATS
#             set `overlap=OVERLAP_FACTOR*(PP-CP)` for symbols begin with VOICED_CONSONATS
OVERLAP_MODE = 'const'
OVERLAP_FACTOR = 0.15

UNVOICED_CONSONATS = {
  'p', 't', 'k'
}
VOICED_CONSONATS = {
  'm', 'n', 'r',
  'y', 'w',
}