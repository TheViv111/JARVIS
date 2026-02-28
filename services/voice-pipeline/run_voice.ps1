$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

Write-Host "Starting JARVIS voice-pipeline on http://127.0.0.1:7788" -ForegroundColor Cyan
python -m uvicorn app.main:app --host 127.0.0.1 --port 7788 --log-level warning --reload

