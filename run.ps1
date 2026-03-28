# Virtual Try-On Application Launcher (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Virtual Try-On Application" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting the application..." -ForegroundColor Yellow
Write-Host "The browser will open automatically at http://localhost:7860" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $PSScriptRoot
python app.py

Read-Host -Prompt "Press Enter to exit"
