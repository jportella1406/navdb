@echo off
setlocal enabledelayedexpansion

set CAE_HOST=10.102.80.1

echo Starting Delete FTP Process...

ftp -n -s:host_delete_script.txt %CAE_HOST%

if errorlevel 1 (
    echo [ERROR] FTP delete failed.
    exit /b 5
)

echo FTP delete completed successfully.
exit /b 0