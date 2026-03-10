$ErrorActionPreference = "Stop"

Set-Location -Path $PSScriptRoot

$pythonExe = "py"
$pythonBaseArgs = @("-3.14")

try {
    & $pythonExe @pythonBaseArgs "--version" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "No se detecto py -3.14"
    }
}
catch {
    $pythonExe = "python"
    $pythonBaseArgs = @()
}

$mainExitCode = 0
$testExitCode = 0

Write-Host "==> Ejecutando analisis principal (main.py)" -ForegroundColor Cyan
& $pythonExe @pythonBaseArgs "main.py"
$mainExitCode = $LASTEXITCODE

Write-Host "`n==> Ejecutando pruebas unitarias" -ForegroundColor Cyan
& $pythonExe @pythonBaseArgs "-m" "unittest" "discover" "-s" "tests" "-p" "test_*.py" "-v"
$testExitCode = $LASTEXITCODE

Write-Host "`n==> Resumen" -ForegroundColor Yellow
Write-Host "main.py exit code: $mainExitCode"
Write-Host "tests exit code:   $testExitCode"

if ($mainExitCode -ne 0 -or $testExitCode -ne 0) {
    Write-Host "Resultado: FALLIDO" -ForegroundColor Red
    exit 1
}

Write-Host "Resultado: OK" -ForegroundColor Green
exit 0

