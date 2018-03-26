@echo off

if "%1"=="1" goto one_console
if "%1"=="2" goto two_console
if "%1"=="3" goto thr_console
if "%1"=="4" goto fou_console

:fou_console
echo Open V-rep with port 20000...
start vrep.exe %2 -gREMOTEAPISERVERSERVICE_20000_FALSE_TRUE "D:\Projects\VREP\RemoteApi_ARIE_Assembly.ttt"

:thr_console
echo Open V-rep with port 19999...
start vrep.exe %2 -gREMOTEAPISERVERSERVICE_19999_FALSE_TRUE "D:\Projects\VREP\RemoteApi_ARIE_Assembly.ttt"

:two_console
echo Open V-rep with port 19998...
start vrep.exe %2 -gREMOTEAPISERVERSERVICE_19998_FALSE_TRUE "D:\Projects\VREP\RemoteApi_ARIE_Assembly.ttt"

:one_console
echo Open V-rep with port 19997...
start vrep.exe %2 -gREMOTEAPISERVERSERVICE_19997_FALSE_TRUE "D:\Projects\VREP\RemoteApi_ARIE_Assembly.ttt"



 