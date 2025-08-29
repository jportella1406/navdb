@echo off
setlocal

REM Ruta del archivo origen
set "ORIGEN=C:\Users\simfinity\Desktop\NDB update for CRJ1\navDB-200"

REM Recibir argumento como destino
set "DESTINO=%~1"

REM Validar si se proporcionó
if not defined DESTINO (
    echo Error: no se especificó carpeta de destino.
    pause
    exit /b
)

REM Copiar archivo
echo Copiando archivo a: %DESTINO%
copy "%ORIGEN%" "%DESTINO%\"

echo.
echo Archivo copiado exitosamente.
exit /b
