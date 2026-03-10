@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%run_all.ps1" >nul 2>&1
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
    echo FALLIDO ^(codigo %EXIT_CODE%^)
    exit /b %EXIT_CODE%
)

echo OK
exit /b 0

