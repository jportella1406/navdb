@echo off
setlocal enabledelayedexpansion

set CAE_HOST=10.102.80.1
set "LOGDIR=C:\Users\josep\OneDrive\Desktop\CAE\navdb\actualizar_ndb\200 01\logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

echo Starting Backup Process...

:: === Timestamp for log ===
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set "dt=%%a"
set "YYYY=%dt:~0,4%"
set "MM=%dt:~4,2%"
set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%"
set "NN=%dt:~10,2%"
set "SS=%dt:~12,2%"
set "STAMP=%YYYY%-%MM%-%DD%_%HH%-%NN%-%SS%"

ftp -n -s:host_backup_script.txt %CAE_HOST% > "%LOGDIR%\backup_%STAMP%.log" 2>&1

if errorlevel 1 (
    echo [ERROR] FTP backup failed. See backup_%STAMP%.log
    exit /b 5
)

echo FTP backup completed successfully. See backup_%STAMP%.log
exit /b 0