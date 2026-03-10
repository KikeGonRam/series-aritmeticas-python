@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ==> Ejecutando flujo completo con run_all.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%run_all.ps1"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo Resultado final: FALLIDO
    exit /b %EXIT_CODE%
)

echo Resultado final: OK
exit /b 0

