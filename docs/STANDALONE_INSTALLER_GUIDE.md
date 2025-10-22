# Creating a Truly Portable Installer

This guide explains how to create a fully self-contained installer that works on ANY Windows PC without requiring Python or any dependencies to be pre-installed.

## The Problem with PyInstaller

PyInstaller cannot bundle:
- TensorRT (system-level CUDA library)
- CUDA runtime libraries
- NVIDIA drivers

This is why you got "TensorRT is not installed" error on the target PC.

## The Solution: Embedded Python with Full Environment

We'll create a package that includes:
1. **Embedded Python 3.10** (no installation needed)
2. **All Python packages** (PyTorch, TensorRT, etc.)
3. **Your application**
4. **Launcher script**

## Option 1: Portable ZIP Package (Recommended)

### Step 1: Build the Portable Package

```powershell
python create_standalone_installer.py
```

This will:
- ✅ Download embedded Python 3.10.11
- ✅ Install pip in the embedded environment
- ✅ Install PyTorch with CUDA 12.4
- ✅ Install TensorRT and all dependencies
- ✅ Copy your application
- ✅ Create launcher scripts
- ✅ Package everything into a ZIP file

### Step 2: Distribute

The script creates: `TensorRT_Converter_Portable.zip` (~2-3 GB)

Users simply:
1. Extract the ZIP
2. Double-click `TensorRT_Converter.bat`
3. Done!

### What's Included

```
TensorRT_Converter/
├── python_embedded/           # Full Python runtime
│   ├── python.exe
│   ├── python310.dll
│   └── Lib/
│       └── site-packages/    # ALL your packages
│           ├── torch/         # PyTorch with CUDA
│           ├── tensorrt/      # TensorRT
│           ├── PyQt5/         # GUI framework
│           └── ...            # Everything else
├── app/
│   ├── src/                  # Your source code
│   └── main.py               # Application entry
├── TensorRT_Converter.bat    # Launcher (click this)
└── README.txt                # Instructions
```

## Option 2: Inno Setup Installer (Professional)

If you want a traditional `.exe` installer with wizard:

### Install Inno Setup

1. Download from: https://jrsoftware.org/isdl.php
2. Install Inno Setup 6

### Build the Installer

First, create the portable package:
```powershell
python create_standalone_installer.py
```

Then compile with Inno Setup:
```powershell
# If Inno Setup is in PATH
iscc installer_config.iss

# Or use the GUI
# Open installer_config.iss in Inno Setup Compiler and click Build
```

This creates: `TensorRT_Converter_Setup.exe`

### Benefits of Inno Setup

- ✅ Professional installer wizard
- ✅ Checks for NVIDIA GPU before installation
- ✅ Creates Start Menu shortcuts
- ✅ Proper uninstaller
- ✅ Smaller download (compressed better)
- ✅ Installs to Program Files

## What the Target PC Needs

The ONLY requirement on the target PC:
- ✅ NVIDIA GPU
- ✅ NVIDIA Drivers (latest recommended)
- ✅ Windows 10/11 64-bit

**Does NOT need:**
- ❌ Python
- ❌ CUDA Toolkit
- ❌ TensorRT installation
- ❌ Any Python packages
- ❌ Visual Studio redistributables

Everything is included!

## Size Comparison

| Method | Size | Install Time | Portability |
|--------|------|--------------|-------------|
| PyInstaller only | ~25 MB | Instant | ❌ Missing TensorRT |
| Portable ZIP | ~2.5 GB | Extract only | ✅ Works everywhere |
| Inno Setup | ~1.5 GB | 2-3 minutes | ✅ Professional |

## Recommended Approach

1. **For quick testing/sharing**: Use the Portable ZIP
2. **For distribution/production**: Use Inno Setup installer
3. **For GitHub releases**: Provide both options

## Troubleshooting

### "Failed to download Python"
Manually download: https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip
Place in project root and run again.

### Build takes too long
This is normal. Installing PyTorch + TensorRT takes 10-15 minutes.
The script downloads ~2 GB of packages.

### Target PC still shows error
Make sure:
1. NVIDIA drivers are installed
2. GPU is working (check Device Manager)
3. All files were extracted from ZIP

## Next Steps

Run this now:
```powershell
python create_standalone_installer.py
```

Then test on another PC!
