$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "Starting JARVIS runtime-api and chat CLI..." -ForegroundColor Cyan

$serverJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    python -m uvicorn app.main:app --host 127.0.0.1 --port 7777
} -ArgumentList $root

try {
    $healthy = $false
    for ($i = 0; $i -lt 30; $i++) {
        if ($serverJob.State -in @("Failed", "Stopped", "Completed")) {
            break
        }

        try {
            $resp = Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:7777/v1/health" -TimeoutSec 2
            if ($resp.status -eq "ok") {
                $healthy = $true
                break
            }
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }

    if (-not $healthy) {
        Write-Host "Runtime API failed to start." -ForegroundColor Red
        $logs = Receive-Job $serverJob -Keep -ErrorAction SilentlyContinue
        if ($logs) {
            Write-Host "Server logs:" -ForegroundColor Yellow
            $logs | ForEach-Object { Write-Host $_ }
        } else {
            Write-Host "No server logs captured." -ForegroundColor Yellow
        }
        Write-Host "If dependencies are missing, run:" -ForegroundColor Yellow
        Write-Host "  pip install -r requirements.txt" -ForegroundColor Gray
        exit 1
    }

    python .\chat_cli.py
}
finally {
    Stop-Job $serverJob -ErrorAction SilentlyContinue | Out-Null
    Remove-Job $serverJob -Force -ErrorAction SilentlyContinue | Out-Null
    Write-Host "Stopped runtime-api." -ForegroundColor DarkGray
}
