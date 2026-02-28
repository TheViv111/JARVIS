$ErrorActionPreference = "Stop"

$runtimeRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$voiceRoot = Join-Path (Split-Path -Parent $runtimeRoot) "voice-pipeline"
Set-Location $runtimeRoot

Write-Host "Starting JARVIS voice interaction stack..." -ForegroundColor Cyan

$voiceJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    python -m uvicorn app.main:app --host 127.0.0.1 --port 7788
} -ArgumentList $voiceRoot

$runtimeJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    python -m uvicorn app.main:app --host 127.0.0.1 --port 7777
} -ArgumentList $runtimeRoot

function Wait-Health([string]$Url, [string]$Name, $Job) {
    for ($i = 0; $i -lt 40; $i++) {
        if ($Job.State -in @("Failed", "Stopped", "Completed")) {
            break
        }
        try {
            $resp = Invoke-RestMethod -Method Get -Uri $Url -TimeoutSec 2
            if ($resp.status -eq "ok") {
                return $true
            }
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }
    Write-Host "$Name failed to start." -ForegroundColor Red
    $logs = Receive-Job $Job -Keep -ErrorAction SilentlyContinue
    if ($logs) {
        Write-Host "$Name logs:" -ForegroundColor Yellow
        $logs | ForEach-Object { Write-Host $_ }
    }
    return $false
}

try {
    $voiceOk = Wait-Health "http://127.0.0.1:7788/v1/health" "voice-pipeline" $voiceJob
    $runtimeOk = Wait-Health "http://127.0.0.1:7777/v1/health" "runtime-api" $runtimeJob
    if (-not ($voiceOk -and $runtimeOk)) {
        Write-Host "Install dependencies:" -ForegroundColor Yellow
        Write-Host "  cd $voiceRoot; pip install -r requirements.txt" -ForegroundColor Gray
        Write-Host "  cd $runtimeRoot; pip install -r requirements.txt" -ForegroundColor Gray
        exit 1
    }

    python .\voice_console.py
}
finally {
    Stop-Job $runtimeJob -ErrorAction SilentlyContinue | Out-Null
    Remove-Job $runtimeJob -Force -ErrorAction SilentlyContinue | Out-Null
    Stop-Job $voiceJob -ErrorAction SilentlyContinue | Out-Null
    Remove-Job $voiceJob -Force -ErrorAction SilentlyContinue | Out-Null
    Write-Host "Stopped JARVIS voice stack." -ForegroundColor DarkGray
}

