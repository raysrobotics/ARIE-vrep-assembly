@echo off
REM 参数%1：需开启几个vrep console  参数%2（可选）：-h 有该参数则不显示图形界面


REM 在这里配置vrep的安装目录，默认为C:\Program Files\V-REP3\V-REP_PRO_EDU\vrep.exe
set VREP="C:\Program Files\V-REP3\V-REP_PRO_EDU\vrep.exe"
set PORT_START=19997
set /a PORT_END=%1+19997-1

for /l %%i in (%PORT_START%, 1, %PORT_END%) do (
REM @echo %%i
echo Open V-rep with scene file RemoteApi_ARIE_Assembly.ttt while listening to port %%i...
start "" %VREP% %2 -gREMOTEAPISERVERSERVICE_%%i_FALSE_TRUE "%cd%\RemoteApi_ARIE_Assembly.ttt"
)

