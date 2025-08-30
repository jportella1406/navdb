@echo off
setlocal

REM Ruta del archivo origen
set "ORIGEN=C:\CAE\configurations\crj200_offer\Load_1_0_1_7_2\Config\J4-Americas\nav1"

REM Recibir argumento como destino
set "DESTINO=C:\Users\simfinity\Desktop\NDB update for CRJ1\navDB-200"

REM Copiar archivo
echo Copying files to: %DESTINO%
copy /Y "%ORIGEN%\fmc_4200_tcpram.bin" "%DESTINO%\" >nul
copy /Y "%ORIGEN%\fmc_4200_nvram.bin" "%DESTINO%\" >nul
copy /Y "%ORIGEN%\fmc_4200_flash.rle" "%DESTINO%\" >nul

echo.
echo Backup completed successfully.
exit /b
