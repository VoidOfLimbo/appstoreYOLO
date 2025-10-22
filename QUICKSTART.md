# TensorRT Model Converter - Quick Start Guide

## Current Installed Packages

Your virtual environment already has most required packages installed:
- ✅ PyTorch (2.9.0)
- ✅ TorchVision (0.24.0)
- ✅ TensorRT (10.13.3.9)
- ✅ PyQt5 (5.15.11)
- ✅ PyInstaller (6.16.0)
- ✅ NumPy (2.2.6)
- ✅ Pillow (12.0.0)
- ✅ ONNX (newly installed)
- ✅ CUDA support (cupy-cuda13x)

## Quick Start

### 1. Run the Application

```powershell
# Make sure you're in the virtual environment
.venv\Scripts\activate

# Run the application
python main.py
```

### 2. Using the GUI

1. The application will automatically detect your GPU and TensorRT installation
2. Drag and drop a model file (.onnx, .pt, .pth) or click "Browse"
3. Select precision mode (FP16 recommended for most GPUs)
4. Adjust workspace size if needed (4GB default)
5. Choose output directory
6. Click "Convert to TensorRT Engine"
7. Monitor progress and wait for completion

### 3. Create Portable Executable (.exe)

To create a standalone executable that can run on any Windows machine:

```powershell
# From the project directory
pyinstaller tensorrt_converter.spec
```

The executable will be in: `dist\TensorRT_Converter\TensorRT_Converter.exe`

**Important**: The executable will still detect hardware on the target machine and optimize accordingly!

### 4. Distribute the Application

To use on another computer:
1. Copy the entire `dist\TensorRT_Converter\` folder
2. Ensure the target machine has:
   - NVIDIA GPU with CUDA support
   - Latest NVIDIA drivers
   - TensorRT runtime installed (can be included in the package)

## Project Structure

```
python/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── tensorrt_converter.spec         # PyInstaller configuration
├── README.md                       # Full documentation
├── QUICKSTART.md                   # This file
├── .gitignore                      # Git ignore rules
│
├── src/                            # Source code
│   ├── __init__.py
│   ├── config.py                   # Application configuration
│   │
│   ├── gui/                        # GUI components
│   │   ├── __init__.py
│   │   └── main_window.py         # Main application window
│   │
│   └── utils/                      # Utility modules
│       ├── __init__.py
│       ├── logger.py              # Logging setup
│       ├── hardware_detector.py   # GPU/CUDA detection
│       └── tensorrt_converter.py  # Model conversion logic
│
├── logs/                           # Application logs (auto-created)
│   └── converter.log
│
├── output/                         # Converted models (default)
│   └── your_model_fp16.engine
│
└── .venv/                          # Virtual environment
```

## Features Implemented

✅ **Hardware-Aware Conversion**
- Automatic GPU detection
- CUDA version check
- TensorRT availability verification
- Compute capability detection
- Recommended precision based on GPU

✅ **User-Friendly GUI**
- Drag & drop support
- File browser
- Real-time progress updates
- Hardware information display
- Conversion settings

✅ **Multiple Input Formats**
- ONNX models (direct conversion)
- PyTorch models (.pt, .pth via ONNX)

✅ **Precision Options**
- FP32 (full precision)
- FP16 (half precision, recommended)
- INT8 (integer precision, fastest)

✅ **Portable Executable**
- PyInstaller spec included
- Hardware detection at runtime
- No Python installation needed on target machine

✅ **Best Practices**
- Modular code structure
- Comprehensive logging
- Error handling
- Type hints
- Documentation

## Testing the Application

### Test 1: Run the GUI
```powershell
python main.py
```
Expected: Window opens showing hardware information

### Test 2: Convert a Model (if you have one)
1. Run the application
2. Load an ONNX or PyTorch model
3. Click convert
4. Check `output/` directory for the .engine file

### Test 3: Build Executable
```powershell
pyinstaller tensorrt_converter.spec
```
Expected: Creates `dist\TensorRT_Converter\` with executable

## Troubleshooting

### "TensorRT not available"
- Ensure TensorRT is properly installed
- Check CUDA compatibility

### "CUDA not detected"
- Update NVIDIA drivers
- Verify GPU is recognized by Windows

### Conversion fails
- Check model format is supported
- Ensure sufficient GPU memory
- Review logs in `logs/converter.log`

### PyInstaller fails
- Ensure all dependencies are installed
- Try: `pip install --upgrade pyinstaller`

## Next Steps

1. ✅ Application is ready to use
2. Test with your YOLO or other models
3. Build the executable with PyInstaller
4. Deploy to target hardware

## Support

Check `logs/converter.log` for detailed error messages and debugging information.
