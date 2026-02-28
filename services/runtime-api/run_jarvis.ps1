$ErrorActionPreference = "Stop"
$root = "C:\Users\vivaa\Documents\jarvis"
Set-Location $root

Write-Host "Launching JARVIS Unified Stack..." -ForegroundColor Cyan
python jarvis.py

