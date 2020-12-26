@echo off
setlocal enabledelayedexpansion

set IPADDR="127.0.0.1"
set MODEL_NAME="dual_round_peg_hole"
set CONF_NUM=0
set X_START=-0.04
set X_END=0.04
set Y_START=-0.04
set Y_END=0.04
set X_PRECISION=5e-3
set Y_PRECISION=5e-3

set PORT_START=19997
set /a PORT_END=%1+19997-1
set COUNT=%1

for /l %%i in (1, 1, %COUNT%) do (
set /a PORT=%PORT_START%+%%i-1
set /a ANGLE=5*%%i-5
start python run_sim.py %MODEL_NAME% --conf_num %CONF_NUM% 20.0 0.0 !ANGLE! --ip-addr %IPADDR% --port !PORT! --precision-x %X_PRECISION% --precision-y %Y_PRECISION% --plot --x-start %X_START% --x-end %X_END% --y-start %Y_START% --y-end %Y_END%
)