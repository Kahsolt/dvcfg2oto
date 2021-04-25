@REM Wrapper script for those who prefer double click rather than commandline typing
@REM Armit 2021/04/25 
@ECHO OFF

SETLOCAL ENABLEDELAYEDEXPANSION

SET DVCFG_PATH=D:\.bin\Apps\UTAU\voice\kori

python dvcfg2oto.py %DVCFG_PATH%
