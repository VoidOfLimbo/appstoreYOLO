# TensorRT Converter - Project Structure

## Root Directory

```
TensorRT_Converter/
├── main.py                     # Application entry point
├── README.md                   # Main documentation
├── requirements.txt            # Python dependencies
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── gui/                   # GUI components
│   │   ├── __init__.py
│   │   └── main_window.py    # Main window and UI
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       ├── hardware_detector.py
│       ├── tensorrt_converter.py
│       └── logger.py
│
├── build_tools/               # Build scripts for all platforms
│   ├── build_all.py          # Master build script
│   ├── build_windows_exe.py  # Windows executable builder
│   ├── build_linux.py        # Linux package builder
│   ├── build_jetson.py       # Jetson package builder
│   └── windows_onefile.spec  # PyInstaller spec (generated)
│
├── docs/                      # Documentation
│   ├── QUICKSTART.md
│   ├── TROUBLESHOOTING.md
│   ├── CUDA_SETUP_GUIDE.md
│   ├── PYINSTALLER_BUILD_GUIDE.md
│   ├── STANDALONE_INSTALLER_GUIDE.md
│   ├── DEPLOYMENT_READY.md
│   └── DEVELOPMENT_GUIDE.md
│
├── config/                    # Configuration files
│   ├── installer_config.iss  # Inno Setup configuration
│   └── LICENSE.txt           # License file
│
├── hooks/                     # PyInstaller hooks
│   └── hook-onnx.py          # ONNX module hook
│
├── assets/                    # Assets (icons, images)
│   └── icon.ico              # Application icon (if exists)
│
├── dist/                      # Build output
│   ├── windows/              # Windows builds
│   ├── linux/                # Linux builds
│   ├── jetson/               # Jetson builds
│   ├── TensorRT_Converter_Windows.exe
│   ├── TensorRT_Converter_Linux.tar.gz
│   └── TensorRT_Converter_Jetson.tar.gz
│
├── logs/                      # Application logs (runtime)
├── output/                    # Converted models (runtime)
│
└── archive/                   # Archived old files
    └── YYYYMMDD_HHMMSS/      # Timestamped archive
```

## Key Files

### Application
- **main.py**: Entry point, initializes and runs the GUI
- **src/gui/main_window.py**: Main PyQt5 GUI with drag-drop, hardware detection, conversion
- **src/utils/tensorrt_converter.py**: Core TensorRT conversion logic
- **src/utils/hardware_detector.py**: GPU/CUDA/TensorRT detection
- **src/config.py**: Application configuration and constants

### Build Tools
- **build_tools/build_all.py**: Interactive builder for all platforms
- **build_tools/build_windows_exe.py**: Creates single-file Windows .exe
- **build_tools/build_linux.py**: Creates Linux x86_64 package
- **build_tools/build_jetson.py**: Creates ARM64 Jetson package

### Documentation
- **README.md**: Main project documentation and usage
- **docs/QUICKSTART.md**: Quick start guide
- **docs/TROUBLESHOOTING.md**: Common issues and solutions
- **docs/CUDA_SETUP_GUIDE.md**: CUDA installation guide
- **docs/DEPLOYMENT_READY.md**: Deployment instructions

## Build Outputs

### Windows
- **Single-file executable**: `dist/windows/TensorRT_Converter_Windows.exe`
- Size: ~500MB - 1GB (includes Python + PyTorch + TensorRT)
- Target: Windows 10/11 64-bit with NVIDIA GPU

### Linux
- **Tarball package**: `dist/TensorRT_Converter_Linux.tar.gz`
- Size: ~10MB (source + scripts)
- Requires: Python installation on target system
- Target: Ubuntu/Debian/Fedora/Arch with NVIDIA GPU

### Jetson
- **Tarball package**: `dist/TensorRT_Converter_Jetson.tar.gz`
- Size: ~10MB (source + scripts)
- Requires: JetPack installed on Jetson device
- Target: Jetson Nano/TX2/Xavier/Orin

## Development Workflow

1. **Edit source code**: Modify files in `src/`
2. **Test locally**: Run `python main.py`
3. **Build for platform**: Run `python build_tools/build_all.py`
4. **Test build**: Test the output in `dist/`
5. **Deploy**: Distribute the platform-specific package

## Clean Project Structure

The following directories are auto-generated and can be deleted:
- `__pycache__/` - Python cache
- `build/` - PyInstaller temporary build files
- `logs/` - Runtime application logs
- `output/` - Converted model outputs

These will be recreated automatically when needed.

---
Last updated: October 22, 2025
