# AppStore Build Script
# This script automates the build and packaging process

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "AppStore Build Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Clean previous builds
Write-Host "[1/4] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "  ✓ Removed build directory" -ForegroundColor Green
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "  ✓ Removed dist directory" -ForegroundColor Green
}
Write-Host ""

# Step 2: Build executable with PyInstaller
Write-Host "[2/4] Building executable with PyInstaller..." -ForegroundColor Yellow
python setup.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ Executable built successfully" -ForegroundColor Green
Write-Host ""

# Step 3: Verify build
Write-Host "[3/4] Verifying build..." -ForegroundColor Yellow
if (Test-Path "dist\AppStore\AppStore.exe") {
    Write-Host "  ✓ AppStore.exe found" -ForegroundColor Green
    $size = (Get-Item "dist\AppStore\AppStore.exe").Length / 1MB
    Write-Host "  ✓ Size: $([math]::Round($size, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "  ✗ Executable not found!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 4: Instructions for creating installer
Write-Host "[4/4] Next steps..." -ForegroundColor Yellow
Write-Host "  To create the installer:" -ForegroundColor White
Write-Host "  1. Install Inno Setup from https://jrsoftware.org/isdl.php" -ForegroundColor White
Write-Host "  2. Open installer\AppStore.iss with Inno Setup" -ForegroundColor White
Write-Host "  3. Click Build -> Compile" -ForegroundColor White
Write-Host "  4. Installer will be in installer\output\" -ForegroundColor White
Write-Host ""

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Executable location: dist\AppStore\" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
