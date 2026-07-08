# Mission Control OS - local dev launcher (Windows / PowerShell)
# Starts the FastAPI backend and the Next.js frontend in separate windows,
# then opens the browser once the web server responds.
# SQLite + mock mode: no Docker or API keys needed.
#
# Usage:  ./dev.ps1     (or double-click dev.cmd)

$ErrorActionPreference = "Stop"
$root   = $PSScriptRoot
$api    = Join-Path $root "apps\api"
$venvPy = Join-Path $api ".venv\Scripts\python.exe"

function Have($name)  { [bool](Get-Command $name -ErrorAction SilentlyContinue) }
function PortBusy($p) { [bool](Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue) }

# --- prerequisites --------------------------------------------------------
$missing = @()
if (-not (Have "node")) { $missing += "Node 20+  (https://nodejs.org)" }
if (-not (Have "pnpm")) { $missing += "pnpm  (npm i -g pnpm)" }
if ($missing.Count -gt 0) {
    Write-Host "Missing prerequisites:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
    exit 1
}
if (-not (Test-Path $venvPy)) {
    Write-Host "Backend venv not found at $venvPy" -ForegroundColor Red
    Write-Host "Set it up first:  cd apps/api;  uv venv;  uv pip install -e `".[dev]`"" -ForegroundColor Yellow
    exit 1
}

# --- port checks ----------------------------------------------------------
foreach ($p in 8000, 3000) {
    if (PortBusy $p) {
        Write-Host "Port $p is already in use. Stop whatever is using it, then retry." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Launching Mission Control OS..." -ForegroundColor Cyan

$apiCmd = "Set-Location `"$api`"; & `"$venvPy`" -m app.seed; & `"$venvPy`" -m uvicorn app.main:app --reload --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $apiCmd

$webCmd = "Set-Location `"$root`"; pnpm --filter web dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $webCmd

# --- wait for web health, then open browser -------------------------------
Write-Host "Waiting for the web server..." -ForegroundColor DarkGray
$ready = $false
for ($i = 0; $i -lt 40; $i++) {
    try { Invoke-WebRequest -UseBasicParsing "http://localhost:3000" -TimeoutSec 2 | Out-Null; $ready = $true; break }
    catch { Start-Sleep -Seconds 1 }
}
if ($ready) { Start-Process "http://localhost:3000" }
else { Write-Host "Web server not up yet; open http://localhost:3000 manually." -ForegroundColor Yellow }

Write-Host ""
Write-Host "  API  ->  http://localhost:8000/docs" -ForegroundColor Green
Write-Host "  Web  ->  http://localhost:3000" -ForegroundColor Green
Write-Host "Close the two spawned windows to stop the servers." -ForegroundColor DarkGray
