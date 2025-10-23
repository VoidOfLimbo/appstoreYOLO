"""
Create a portable Windows package with setup script.
This approach doesn't require Inno Setup and works immediately.
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

def print_step(message):
    """Print a step message."""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")

def create_setup_script():
    """Create the setup.bat script."""
    
    setup_script = """@echo off
REM TensorRT Model Converter - Portable Setup Script
REM This script sets up the application on first run

echo ============================================================
echo   TensorRT Model Converter - First Time Setup
echo ============================================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.10 or 3.11 from python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found

REM Check for NVIDIA driver
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: NVIDIA driver not detected!
    echo This application requires an NVIDIA GPU with CUDA support.
    echo.
    echo Do you want to continue anyway? (Y/N)
    set /p continue=
    if /i not "!continue!"=="Y" (
        exit /b 1
    )
) else (
    echo [OK] NVIDIA driver detected
)

echo.
echo ============================================================
echo   Creating Virtual Environment
echo ============================================================
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
call .venv\\Scripts\\activate.bat

echo.
echo ============================================================
echo   Installing Dependencies
echo ============================================================
echo.
echo This will take 5-10 minutes depending on your internet speed.
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install PyTorch with CUDA
echo.
echo Installing PyTorch with CUDA support (large download)...
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
if errorlevel 1 (
    echo ERROR: Failed to install PyTorch
    pause
    exit /b 1
)

REM Install other requirements
echo.
echo Installing other dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo You can now run the application using:
echo   - Double-click: TensorRT_Converter.bat
echo   - Or create a desktop shortcut to TensorRT_Converter.bat
echo.
pause

REM Run the application
TensorRT_Converter.bat
"""
    return setup_script

def create_launcher_script():
    """Create the launcher script."""
    
    launcher_script = """@echo off
REM TensorRT Model Converter Launcher

cd /d "%~dp0"

REM Check if setup has been run
if not exist ".venv\\Scripts\\python.exe" (
    echo First time setup required!
    echo.
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment and run
call .venv\\Scripts\\activate.bat
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
"""
    return launcher_script

def create_readme():
    """Create README for the portable package."""
    
    readme = """# TensorRT Model Converter - Portable Package

## Quick Start

1. **First Time Setup** (Only once):
   - Double-click `setup.bat`
   - Wait 5-10 minutes for installation
   - Setup will:
     * Check for Python and NVIDIA drivers
     * Create virtual environment
     * Install PyTorch with CUDA
     * Install all dependencies

2. **Run Application**:
   - Double-click `TensorRT_Converter.bat`
   - Application will start with full CUDA support

## System Requirements

- Windows 10/11 (64-bit)
- Python 3.10 or 3.11 (Download from python.org)
- NVIDIA GPU with CUDA support
- NVIDIA Drivers (525.60 or newer)
- 5 GB free disk space
- Internet connection (for first-time setup)

## Installation Steps

### 1. Install Python (if not already installed)

- Download Python 3.10 or 3.11 from https://www.python.org/downloads/
- During installation, CHECK "Add Python to PATH"
- Verify: Open CMD and type `python --version`

### 2. Install NVIDIA Drivers (if not already installed)

- Download latest drivers from https://www.nvidia.com/Download/index.aspx
- Install and restart your computer

### 3. Run Setup

- Extract this ZIP to a folder (e.g., C:\\TensorRT_Converter)
- Right-click `setup.bat` → Run as Administrator
- Follow on-screen instructions
- Wait for installation to complete

### 4. Launch Application

- Double-click `TensorRT_Converter.bat`
- Application will detect your GPU and be ready to use

## Features

- Convert YOLO models to TensorRT engine format
- Export to ONNX, TorchScript, OpenVINO
- Automatic GPU detection and optimization
- Drag & drop interface
- Batch processing support
- Custom image sizes and precision settings

## Troubleshooting

### "Python not found"
- Install Python 3.10 or 3.11 from python.org
- Ensure "Add Python to PATH" was checked
- Restart computer after installation

### "NVIDIA driver not detected"
- Install latest NVIDIA drivers
- Restart computer
- Run `nvidia-smi` in CMD to verify

### Setup fails during pip install
- Check internet connection
- Run setup.bat as Administrator
- Temporarily disable antivirus
- Delete .venv folder and run setup again

### Application won't start
- Ensure setup.bat completed successfully
- Check that .venv folder exists
- Run TensorRT_Converter.bat from CMD to see error messages

## Updating

To update the application:
1. Download new version
2. Extract to same folder (overwrite files)
3. Run setup.bat again to update dependencies

## Uninstalling

Simply delete the entire folder. No registry entries or system files are created.

## Portable Usage

This package is fully portable:
- Can be copied to USB drive
- Can be moved to different locations
- Each copy maintains its own virtual environment
- No system-wide installation required

## File Structure

```
TensorRT_Converter/
├── setup.bat              # First-time setup (run once)
├── TensorRT_Converter.bat # Application launcher
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── README.txt            # This file
├── src/                   # Application source code
├── config/                # Configuration files
├── docs/                  # Documentation
└── .venv/                 # Virtual environment (created by setup)
```

## Support

For issues or questions:
- GitHub: https://github.com/VoidOfLimbo/appstoreYOLO
- Check docs/ folder for detailed documentation

## License

This software is provided as-is for model conversion purposes.
"""
    return readme

def create_portable_package():
    """Create the portable package."""
    
    print_step("Creating Portable Windows Package")
    
    base_dir = Path(__file__).parent.parent
    dist_dir = base_dir / "dist"
    package_dir = dist_dir / "TensorRT_Converter_Portable"
    
    # Create dist directory
    dist_dir.mkdir(exist_ok=True)
    
    # Remove old package if exists
    if package_dir.exists():
        print("Removing old package...")
        shutil.rmtree(package_dir)
    
    # Create package directory
    print(f"Creating package directory: {package_dir}")
    package_dir.mkdir()
    
    # Copy application files
    print("\nCopying application files...")
    
    files_to_copy = [
        "main.py",
        "requirements.txt",
    ]
    
    for file in files_to_copy:
        src = base_dir / file
        dst = package_dir / file
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✓ {file}")
    
    # Copy directories
    dirs_to_copy = ["src", "config", "docs"]
    
    for dir_name in dirs_to_copy:
        src = base_dir / dir_name
        dst = package_dir / dir_name
        if src.exists():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'))
            print(f"  ✓ {dir_name}/")
    
    # Create setup script
    print("\nCreating setup script...")
    setup_bat = package_dir / "setup.bat"
    setup_bat.write_text(create_setup_script(), encoding='utf-8')
    print("  ✓ setup.bat")
    
    # Create launcher script
    print("Creating launcher script...")
    launcher_bat = package_dir / "TensorRT_Converter.bat"
    launcher_bat.write_text(create_launcher_script(), encoding='utf-8')
    print("  ✓ TensorRT_Converter.bat")
    
    # Create README
    print("Creating README...")
    readme_txt = package_dir / "README.txt"
    readme_txt.write_text(create_readme(), encoding='utf-8')
    print("  ✓ README.txt")
    
    # Create output directory
    output_dir = package_dir / "output"
    output_dir.mkdir()
    (output_dir / "README.txt").write_text("Converted models will be saved here by default.", encoding='utf-8')
    print("  ✓ output/")
    
    # Create ZIP archive
    print_step("Creating ZIP Archive")
    
    zip_path = dist_dir / "TensorRT_Converter_Portable.zip"
    if zip_path.exists():
        zip_path.unlink()
    
    print(f"Creating: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    # Get size
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    print_step("Package Created Successfully!")
    
    print(f"""
✅ Portable package created!

📦 Package Location:
   {package_dir}

📦 ZIP Archive:
   {zip_path}
   Size: {zip_size_mb:.1f} MB

📋 What's Included:
   ✓ Application source code
   ✓ setup.bat (first-time setup)
   ✓ TensorRT_Converter.bat (launcher)
   ✓ README.txt (user guide)
   ✓ All documentation

🚀 To Use:
   1. Extract ZIP to any folder
   2. Run setup.bat (one time only)
   3. Run TensorRT_Converter.bat to start

📦 To Distribute:
   Share the ZIP file ({zip_size_mb:.1f} MB)
   Users need:
   - Python 3.10/3.11
   - NVIDIA Drivers
   - Internet (for setup)

💡 Benefits:
   ✓ No Inno Setup required
   ✓ Fully portable
   ✓ Proper CUDA support
   ✓ Easy to update
   ✓ Small download size
""")
    
    return True

def main():
    """Main function."""
    try:
        if create_portable_package():
            return 0
        else:
            return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
