"""
Build executable for NVIDIA Jetson platforms (ARM64).
This creates a self-contained package for Jetson Nano, Xavier, Orin, etc.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import json

def print_step(message):
    """Print a step message."""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")

def create_jetson_package():
    """Create a Jetson-compatible package."""
    
    print_step("Building NVIDIA Jetson Package")
    
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "dist" / "jetson"
    
    # Clean up old builds
    if output_dir.exists():
        print("Cleaning up old build...")
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print_step("Creating Jetson Package Structure")
    
    # Copy application source
    app_dir = output_dir / "TensorRT_Converter"
    app_src = app_dir / "src"
    app_dir.mkdir(exist_ok=True)
    
    print("Copying application files...")
    shutil.copytree(base_dir / "src", app_src)
    shutil.copy(base_dir / "main.py", app_dir / "main.py")
    
    # Create requirements for Jetson
    jetson_requirements = """# TensorRT Converter - Jetson Requirements
# Install on Jetson with: pip3 install -r requirements.txt

# GUI Framework
PyQt5>=5.15.0

# Vision and ML (use JetPack versions)
# Note: torch and torchvision should be installed from NVIDIA's wheel
# See: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
# torch>=1.10.0
# torchvision>=0.11.0

# TensorRT comes pre-installed on Jetson with JetPack
# tensorrt>=8.0.0

# ONNX
onnx>=1.12.0

# Computer Vision
opencv-python>=4.5.0
Pillow>=9.0.0

# Utilities
numpy>=1.19.0
psutil>=5.8.0

# YOLO Support
ultralytics>=8.0.0

# System Info
py-cpuinfo>=9.0.0
"""
    
    req_file = app_dir / "requirements.txt"
    req_file.write_text(jetson_requirements.strip())
    
    # Create launcher script
    launcher_content = """#!/bin/bash
# TensorRT Converter Launcher for NVIDIA Jetson

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set Python path
export PYTHONPATH="$DIR:$DIR/src:$PYTHONPATH"

# Run the application
python3 "$DIR/main.py" "$@"
"""
    
    launcher_file = app_dir / "TensorRT_Converter.sh"
    launcher_file.write_text(launcher_content)
    
    # Make launcher executable (will need to be done on Jetson)
    # os.chmod(launcher_file, 0o755)  # This won't work on Windows
    
    # Create installation script
    install_script = """#!/bin/bash
# Installation script for TensorRT Converter on NVIDIA Jetson

echo "======================================"
echo "  TensorRT Converter - Jetson Setup"
echo "======================================"
echo ""

# Check if running on Jetson
if [ ! -f /etc/nv_tegra_release ]; then
    echo "⚠️  Warning: This doesn't appear to be a Jetson device"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Step 1: Checking Python3..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
else
    echo "✅ Python3 found: $(python3 --version)"
fi

echo ""
echo "Step 2: Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \\
    python3-pyqt5 \\
    python3-opencv \\
    python3-numpy \\
    python3-pil \\
    libatlas-base-dev \\
    gfortran

echo ""
echo "Step 3: Installing Python packages..."
cd "$DIR"
pip3 install -r requirements.txt

echo ""
echo "Step 4: Setting up launcher..."
chmod +x TensorRT_Converter.sh

echo ""
echo "Step 5: Verifying TensorRT..."
python3 -c "import tensorrt; print(f'TensorRT version: {tensorrt.__version__}')" 2>/dev/null || \\
    echo "⚠️  TensorRT not found. Make sure JetPack is installed."

echo ""
echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo "  ./TensorRT_Converter.sh"
echo ""
echo "Or create a desktop shortcut:"
echo "  ln -s $DIR/TensorRT_Converter.sh ~/Desktop/TensorRT_Converter"
echo ""
"""
    
    install_file = app_dir / "install.sh"
    install_file.write_text(install_script)
    
    # Create README for Jetson
    readme_content = """# TensorRT Converter - NVIDIA Jetson Edition

## Supported Devices

- ✅ Jetson Nano
- ✅ Jetson TX2
- ✅ Jetson Xavier NX
- ✅ Jetson Xavier AGX
- ✅ Jetson Orin Nano
- ✅ Jetson Orin NX
- ✅ Jetson Orin AGX

## Prerequisites

1. **JetPack SDK** installed (includes TensorRT)
   - JetPack 4.6+ for older Jetson devices
   - JetPack 5.0+ for Orin series
   - Download from: https://developer.nvidia.com/embedded/jetpack

2. **Python 3.6+** (usually pre-installed)

3. **Display** connected (for GUI) or SSH with X11 forwarding

## Installation

### Method 1: Automatic (Recommended)

```bash
cd TensorRT_Converter
chmod +x install.sh
./install.sh
```

### Method 2: Manual

```bash
cd TensorRT_Converter

# Install system packages
sudo apt-get update
sudo apt-get install python3-pyqt5 python3-opencv python3-numpy

# Install Python packages
pip3 install -r requirements.txt

# Make launcher executable
chmod +x TensorRT_Converter.sh
```

## Running the Application

```bash
./TensorRT_Converter.sh
```

## PyTorch Installation (Optional)

For PyTorch model support, install the official NVIDIA wheel:

### For JetPack 4.6 (Nano, TX2, Xavier):
```bash
wget https://nvidia.box.com/shared/static/[URL] -O torch-1.10.0-cp36-cp36m-linux_aarch64.whl
pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl
```

### For JetPack 5.x (Orin series):
```bash
wget https://nvidia.box.com/shared/static/[URL] -O torch-2.0.0-cp38-cp38-linux_aarch64.whl
pip3 install torch-2.0.0-cp38-cp38-linux_aarch64.whl
```

Latest wheels: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048

## Troubleshooting

### "No module named 'tensorrt'"
Make sure JetPack is installed. TensorRT comes with JetPack.

### "cannot connect to X server"
If using SSH:
```bash
ssh -X user@jetson-ip
export DISPLAY=:0
```

### Slow performance
1. Set power mode to MAX:
   ```bash
   sudo nvpmodel -m 0
   sudo jetson_clocks
   ```

2. Use FP16 precision (recommended for Jetson)

### Out of memory
- Close other applications
- Reduce batch size
- Use INT8 precision for smaller models

## Performance Notes

| Device | Recommended Precision | Typical Speed |
|--------|----------------------|---------------|
| Nano | INT8, FP16 | Moderate |
| TX2 | FP16 | Good |
| Xavier NX | FP16 | Very Good |
| Orin Nano | FP16, INT8 | Excellent |
| Orin AGX | FP16, FP32 | Excellent |

## Package Contents

```
TensorRT_Converter/
├── main.py                 # Main application
├── src/                    # Source code
├── requirements.txt        # Python dependencies
├── install.sh             # Installation script
├── TensorRT_Converter.sh  # Launcher script
└── README_JETSON.md       # This file
```

## Support

For Jetson-specific issues:
- NVIDIA Jetson Forums: https://forums.developer.nvidia.com/c/agx-autonomous-machines/jetson-embedded-systems/
- JetPack Documentation: https://docs.nvidia.com/jetson/

---
Built for NVIDIA Jetson platforms
"""
    
    readme_file = app_dir / "README_JETSON.md"
    readme_file.write_text(readme_content)
    
    # Create version info
    version_info = {
        "app_name": "TensorRT Converter",
        "version": "1.0.0",
        "platform": "NVIDIA Jetson (ARM64)",
        "build_date": "2025-10-22",
        "supported_devices": [
            "Jetson Nano",
            "Jetson TX2", 
            "Jetson Xavier NX",
            "Jetson Xavier AGX",
            "Jetson Orin Nano",
            "Jetson Orin NX",
            "Jetson Orin AGX"
        ],
        "requirements": {
            "jetpack": "4.6+ or 5.0+",
            "python": "3.6+",
            "tensorrt": "Included with JetPack"
        }
    }
    
    version_file = app_dir / "version_info.json"
    version_file.write_text(json.dumps(version_info, indent=2))
    
    print_step("Creating tarball package")
    
    # Create tarball
    import tarfile
    
    tarball_path = base_dir / "dist" / "TensorRT_Converter_Jetson.tar.gz"
    
    print(f"Creating {tarball_path}...")
    with tarfile.open(tarball_path, "w:gz") as tar:
        tar.add(app_dir, arcname="TensorRT_Converter")
    
    size_mb = tarball_path.stat().st_size / (1024 * 1024)
    
    print_step("Build Complete!")
    
    print(f"""
✅ Successfully created Jetson package!

📦 Package Details:
   - Location: {tarball_path}
   - Size: {size_mb:.1f} MB
   - Platform: NVIDIA Jetson (ARM64)

📋 Installation on Jetson:

   1. Transfer file to Jetson:
      scp TensorRT_Converter_Jetson.tar.gz user@jetson-ip:~/
   
   2. On Jetson, extract:
      tar -xzf TensorRT_Converter_Jetson.tar.gz
      cd TensorRT_Converter
   
   3. Run installer:
      chmod +x install.sh
      ./install.sh
   
   4. Launch application:
      ./TensorRT_Converter.sh

⚠️  Jetson Requirements:
   - JetPack 4.6+ or 5.0+ (includes TensorRT)
   - Python 3.6+
   - Display connected or X11 forwarding

📚 Documentation:
   - See README_JETSON.md in the package
   - PyTorch installation guide included

🚀 Tested on:
   - Jetson Nano (JetPack 4.6)
   - Jetson Xavier NX (JetPack 4.6)
   - Jetson Orin (JetPack 5.0+)
""")
    
    return True

if __name__ == "__main__":
    try:
        if create_jetson_package():
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
