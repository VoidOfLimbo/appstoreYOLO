# Quick Development Test Script
# Run this to quickly test the application during development

Write-Host "Starting AppStore in development mode..." -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment if it exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
}

# Run the application
Write-Host "Launching application..." -ForegroundColor Green
python main.py
