@echo off

set PYTHON_EXE="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Anaconda3_64\python.exe"
set PYTHON_CWP="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Anaconda3_64\cwp.py"
set PYTHON_DIR="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Anaconda3_64"
set CMD_EXE=%windir%\system32\cmd.exe

echo Running Anaconda Python Environment...
call %PYTHON_EXE% %PYTHON_CWP% %PYTHON_DIR% %CMD_EXE% "/K" "activate py3-cntk"