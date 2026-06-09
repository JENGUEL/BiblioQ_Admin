# Install Supabase CLI on Windows without Scoop/npm.
# Downloads the official binary from GitHub and adds it to the user PATH.

$ErrorActionPreference = "Stop"
$installDir = Join-Path $env:LOCALAPPDATA "Programs\supabase"
New-Item -ItemType Directory -Force -Path $installDir | Out-Null

Write-Host "Fetching latest Supabase CLI release..." -ForegroundColor Cyan
$release = Invoke-RestMethod -Uri "https://api.github.com/repos/supabase/cli/releases/latest"
$asset = $release.assets | Where-Object { $_.name -match "windows_amd64" -and $_.name -match "\.tar\.gz$" } | Select-Object -First 1
if (-not $asset) {
    $asset = $release.assets | Where-Object { $_.name -match "windows_amd64" } | Select-Object -First 1
}
if (-not $asset) {
    throw "Could not find a Windows amd64 asset in the latest release."
}

$archive = Join-Path $env:TEMP $asset.name
Write-Host "Downloading $($asset.name)..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $archive -UseBasicParsing

$extractDir = Join-Path $env:TEMP "supabase-cli-extract"
if (Test-Path $extractDir) { Remove-Item -Recurse -Force $extractDir }
New-Item -ItemType Directory -Force -Path $extractDir | Out-Null

if ($asset.name -like "*.tar.gz") {
    tar -xzf $archive -C $extractDir
} elseif ($asset.name -like "*.zip") {
    Expand-Archive -Path $archive -Force -DestinationPath $extractDir
} else {
    throw "Unsupported archive format: $($asset.name)"
}

$exes = Get-ChildItem -Path $extractDir -Recurse -Filter "*.exe"
if (-not $exes) {
    throw "No executables found in downloaded archive."
}

foreach ($bin in $exes) {
    Copy-Item $bin.FullName (Join-Path $installDir $bin.Name) -Force
    Write-Host "  -> $($bin.Name)" -ForegroundColor DarkGray
}

if (-not (Test-Path (Join-Path $installDir "supabase-go.exe"))) {
    throw "supabase-go.exe missing after install. Re-download the full release tarball."
}

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
    $env:Path = "$env:Path;$installDir"
}

Write-Host ""
Write-Host "Installed to: $installDir\supabase.exe" -ForegroundColor Green
& (Join-Path $installDir "supabase.exe") --version
Write-Host ""
Write-Host "Close and reopen PowerShell, then run:" -ForegroundColor Yellow
Write-Host "  supabase login"
Write-Host "  cd BiblioQ_Admin"
Write-Host "  supabase link --project-ref kexuogfefmtndgmjqrdo"
