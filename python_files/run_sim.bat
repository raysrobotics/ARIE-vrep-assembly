@echo off
setlocal enabledelayedexpansion

set IPADDR="127.0.0.1"
set PEG_PATH="D:/Projects/3D models/simbody_test/tri_peg_hole/peg_tri_r_200_h_801.stl"
set HOL_PATH="D:/Projects/3D models/simbody_test/tri_peg_hole/hol_tri_r_201_h_901.stl"
set X_START=-0.04
set X_END=0.04
set Y_START=-0.04
set Y_END=0.04
set X_PRECISION=5e-4
set Y_PRECISION=5e-4

set PORT_START=19997
set /a PORT_END=%1+19997-1
set COUNT=%1

for /l %%i in (0, 1, %COUNT%) do (
set /a PORT=%PORT_START%+%%i
set /a ANGLE=5*%%i
start python run_sim.py %PEG_PATH% %HOL_PATH% 0.0 15.0 !ANGLE! --ip-addr %IPADDR% --port !PORT! --precision-x %X_PRECISION% --precision-y %Y_PRECISION% --plot --x-start %X_START% --x-end %X_END% --y-start %Y_START% --y-end %Y_END%
)