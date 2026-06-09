# BiblioQ Admin — Supabase deploy helper (uses installed CLI binary).
# Run from BiblioQ_Admin folder after: supabase login + supabase link

$ErrorActionPreference = "Stop"
$sb = Join-Path $env:LOCALAPPDATA "Programs\supabase\supabase.exe"
if (-not (Test-Path $sb)) {
    throw "Supabase CLI not found. Run scripts/install_supabase_cli.ps1 first."
}

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

function Invoke-Supabase {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    & $sb @Args
}

Write-Host "Project: $root" -ForegroundColor Cyan
Write-Host "Using: $sb" -ForegroundColor DarkGray
Write-Host ""

if ($args.Count -eq 0) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\scripts\deploy_supabase.ps1 link"
    Write-Host "  .\scripts\deploy_supabase.ps1 db-push"
    Write-Host "  .\scripts\deploy_supabase.ps1 secrets"
    Write-Host "  .\scripts\deploy_supabase.ps1 functions"
    Write-Host "  .\scripts\deploy_supabase.ps1 all"
    exit 0
}

$cmd = $args[0]

switch ($cmd) {
    "link" {
        Invoke-Supabase link --project-ref kexuogfefmtndgmjqrdo
    }
    "db-push" {
        Invoke-Supabase db push
    }
    "secrets" {
        if (-not $env:SUPABASE_SERVICE_ROLE_KEY) {
            Write-Host "Set env var first (paste service_role JWT from dashboard):" -ForegroundColor Yellow
            Write-Host '  $env:SUPABASE_SERVICE_ROLE_KEY = "eyJ..."'
            exit 1
        }
        $tokens = & "$PSScriptRoot\generate_api_tokens.ps1" | Out-String
        Write-Host $tokens
        Write-Host "Then run secrets set manually with your tokens and service role key." -ForegroundColor Yellow
    }
    "functions" {
        Invoke-Supabase functions deploy agent_checkin --no-verify-jwt --use-api
        Invoke-Supabase functions deploy agent_command_result --no-verify-jwt --use-api
        Invoke-Supabase functions deploy agent_crash_report --no-verify-jwt --use-api
        Invoke-Supabase functions deploy admin_revoke_license --no-verify-jwt --use-api
        Invoke-Supabase functions deploy admin_restore_license --no-verify-jwt --use-api
        Invoke-Supabase functions deploy admin_queue_command --no-verify-jwt --use-api
    }
    "all" {
        & $PSScriptRoot\deploy_supabase.ps1 db-push
        & $PSScriptRoot\deploy_supabase.ps1 functions
    }
    default {
        Invoke-Supabase @args
    }
}
