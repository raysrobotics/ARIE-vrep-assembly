# 这个文件没用！！！


#./vrep_files/run_vrep.bat 1 -h ; Start-Sleep -Seconds 10 ; ./python_files/run_sim.bat 1

$code = { ./vrep_files/run_vrep.bat 1 -h } 
$job = Start-Job -ScriptBlock $code

$text="$(get-date) - start verp... wait 10 sec to start the simulation..."
$text
Start-Sleep -Seconds 5

./python_files/run_sim.bat 1