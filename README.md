# TensorRT Model Converter

A GUI application for converting machine learning models to TensorRT engine format for optimized inference on NVIDIA GPUs.

## Features

- **Hardware-Aware Conversion**: Automatically detects GPU capabilities and recommends optimal precision settings
- **Multiple Input Formats**: Supports ONNX, PyTorch (.pt, .pth) models
- **Drag & Drop Interface**: User-friendly GUI with drag-and-drop support
- **Precision Options**: Support for FP32, FP16, and INT8 precision modes
- **Portable Executable**: Can be compiled to standalone .exe for easy distribution
- **Progress Tracking**: Real-time conversion progress and logging

## Requirements

- Python 3.10+
- NVIDIA GPU with CUDA support
- TensorRT installed
- Windows OS (for .exe build)

## Installation

1. Clone the repository or extract the files
2. Create a virtual environment (optional but recommended):
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

### Running from Python

```powershell
python main.py
```

### Creating an Executable

To create a standalone .exe file:

```powershell
pyinstaller tensorrt_converter.spec
```

The executable will be created in the `dist/TensorRT_Converter/` directory.

### Using the Application

1. **Launch the application**: Run `main.py` or the compiled executable
2. **Check Hardware Info**: The application will automatically detect your GPU and recommend settings
3. **Select Model**: Drag & drop a model file or use the Browse button
4. **Configure Settings**:
   - Choose precision mode (FP32, FP16, or INT8)
   - Set workspace size (higher = more optimization opportunities)
   - Select output directory
5. **Convert**: Click "Convert to TensorRT Engine" button
6. **Monitor Progress**: Watch the conversion progress in real-time
7. **Use Engine**: The optimized .engine file will be saved to the output directory

## Supported Model Formats

- **ONNX** (.onnx): Direct conversion to TensorRT
- **PyTorch** (.pt, .pth): Converts via ONNX intermediate format

## Project Structure

```
.
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── tensorrt_converter.spec # PyInstaller specification
├── src/
│   ├── config.py          # Configuration settings
│   ├── gui/
│   │   └── main_window.py # GUI implementation
│   └── utils/
│       ├── hardware_detector.py    # Hardware detection
│       ├── tensorrt_converter.py   # Conversion logic
│       └── logger.py               # Logging setup
├── logs/                   # Application logs
└── output/                 # Default output directory
```

## Hardware Awareness

The application automatically:
- Detects available CUDA GPUs
- Checks TensorRT availability
- Determines GPU compute capability
- Recommends optimal precision based on hardware
- Validates conversion compatibility before processing

## Precision Modes

- **FP32**: Full precision, best accuracy, larger models
- **FP16**: Half precision, good balance, recommended for modern GPUs
- **INT8**: Integer precision, fastest inference, requires calibration (advanced)

## Troubleshooting

### TensorRT Not Available
Ensure TensorRT is properly installed and compatible with your CUDA version.

### CUDA Not Detected
Verify NVIDIA drivers are installed and CUDA is accessible.

### Conversion Fails
- Check model format is supported
- Ensure sufficient GPU memory
- Review logs in `logs/converter.log`

## Building for Distribution

The application can be packaged as a standalone executable that includes all dependencies:

1. Ensure PyInstaller is installed: `pip install pyinstaller`
2. Run: `pyinstaller tensorrt_converter.spec`
3. Distribute the entire `dist/TensorRT_Converter/` folder

The executable is hardware-aware and will detect capabilities on the target machine.

## License

This project is provided as-is for educational and commercial use.

## Version

Current version: 1.0.0
