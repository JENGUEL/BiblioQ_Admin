# Install BiblioQ Agent as Windows service (run as Administrator)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $Root "..\..\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

Write-Host "Installing BiblioQ Agent service..."
& $Python (Join-Path $Root "service_win.py") install
& $Python (Join-Path $Root "service_win.py") start
Write-Host "Done. Configure agent config at %LOCALAPPDATA%\BiblioQ\agent\config.json"
