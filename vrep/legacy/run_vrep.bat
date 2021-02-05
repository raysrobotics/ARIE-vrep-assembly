@echo off
echo "Usage: run_vrep [num_of_instance] (-h)"
echo "[num_of_instance]: The number of vrep consoles to launch"
echo "-h: (optional) Run vrep in headless mode"
REM Param%1：The number of vrep consoles to launch  Param%2(optional)：-h Run vrep in headless mode

REM Please specify the install path of vrep executable. The default value is:
REM C:\Program Files\V-REP3\V-REP_PRO_EDU\vrep.exe
@REM set VREP="C:\Program Files\V-REP3\V-REP_PRO_EDU\vrep.exe"
set VREP="C:\Program Files\CoppeliaRobotics\CoppeliaSimEdu\coppeliaSim.exe"


REM The following parameters should not be modified unless you know what you should change accordingly
REM The port corresponding to the vrep instance. The first instance uses port 19997, the second 19998,...
set PORT_START=19997
set /a PORT_END=%1+19997-1

for /l %%i in (%PORT_START%, 1, %PORT_END%) do (
REM @echo %%i
echo Open V-rep with scene file RemoteApi_ARIE_Assembly.ttt while listening to port %%i...
start "" %VREP% %2 -gREMOTEAPISERVERSERVICE_%%i_FALSE_TRUE "%cd%\RemoteApi_ARIE_Assembly.ttt"
)

