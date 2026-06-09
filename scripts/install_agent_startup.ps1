# BiblioQ Agent — manual startup repair script
# Run in PowerShell (no admin required for HKCU + ONLOGON task):
#   powershell -ExecutionPolicy Bypass -File install_agent_startup.ps1 -InstallDir "C:\Program Files\BiblioQ"

param(
    [string]$InstallDir = "C:\Program Files\BiblioQ"
)

$ErrorActionPreference = "Stop"
$agentExe = Join-Path $InstallDir "agent\BiblioQAgent.exe"
if (-not (Test-Path $agentExe)) {
    Write-Error "BiblioQAgent.exe not found at $agentExe"
}

$scriptDir = Join-Path $env:ProgramData "BiblioQ\agent"
New-Item -ItemType Directory -Force -Path $scriptDir | Out-Null
$scriptPath = Join-Path $scriptDir "start_agent.ps1"

@(
    "`$exe = '$($agentExe -replace '''', '''''')'"
    'if (Test-Path $exe) {'
    '  $dir = Split-Path $exe'
    '  Start-Process -FilePath $exe -WindowStyle Hidden -WorkingDirectory $dir'
    '}'
) | Set-Content -Path $scriptPath -Encoding UTF8

$launch = "powershell -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""

schtasks /Create /TN BiblioQAgentLogon /TR $launch /SC ONLOGON /RL HIGHEST /F
Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name BiblioQAgent -Value $launch

Start-Process powershell -ArgumentList @('-NoProfile', '-WindowStyle', 'Hidden', '-ExecutionPolicy', 'Bypass', '-File', $scriptPath) -WindowStyle Hidden

Write-Host "Agent startup registered. Script: $scriptPath"
Write-Host "Agent exe: $agentExe"
