@echo off
setlocal

REM Ruta del archivo origen
set "ORIGEN=C:\Users\josep\OneDrive\Desktop\UTP\2025\plantilla actualizada.docx"

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
