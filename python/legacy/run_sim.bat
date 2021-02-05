@echo off
setlocal enabledelayedexpansion

set IPADDR="127.0.0.1"
set MODEL_NAME="rounded_rectangle_peg_hole"
set CONF_NUM=1
set X_START=-0.04
set X_END=0.04
set Y_START=-0.04
set Y_END=0.04
set X_PRECISION=5e-4
set Y_PRECISION=5e-4

set PORT_START=19997
set /a PORT_END=%1+19997-1
set COUNT=%1

for /l %%i in (1, 1, %COUNT%) do (
set /a PORT=%PORT_START%+%%i-1
set /a ANGLE=1*%%i-1
start python run_sim.py %MODEL_NAME% --conf_num %CONF_NUM% !ANGLE! 0.0 0.0  --ip-addr %IPADDR% --port !PORT! --precision-x %X_PRECISION% --precision-y %Y_PRECISION% --plot --x-start %X_START% --x-end %X_END% --y-start %Y_START% --y-end %Y_END%
)