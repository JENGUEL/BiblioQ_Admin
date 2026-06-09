# Generate BiblioQ Admin custom API tokens (NOT Supabase dashboard keys).
# Run once, then use the same values in edge function secrets + app/agent config.

$agentKey = -join ((48..57 + 65..90 + 97..122 | Get-Random -Count 32 | ForEach-Object { [char]$_ }))
$adminToken = -join ((48..57 + 65..90 + 97..122 | Get-Random -Count 32 | ForEach-Object { [char]$_ }))

Write-Host ""
Write-Host "=== BiblioQ custom tokens (save these securely) ===" -ForegroundColor Cyan
Write-Host "AGENT_API_KEY:   $agentKey"
Write-Host "ADMIN_API_TOKEN: $adminToken"
Write-Host ""
Write-Host "Set edge function secrets:" -ForegroundColor Yellow
Write-Host "  supabase secrets set AGENT_API_KEY=$agentKey ADMIN_API_TOKEN=$adminToken"
Write-Host ""
Write-Host "Agent config (%LOCALAPPDATA%\BiblioQ\agent\config.json):" -ForegroundColor Yellow
Write-Host "  `"agent_api_key`": `"$agentKey`""
Write-Host ""
Write-Host "Admin app Settings -> Agent API key / Admin API token" -ForegroundColor Yellow
