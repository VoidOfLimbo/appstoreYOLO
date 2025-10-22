"""
Build executable for Linux (x86_64) platforms.
Creates an AppImage or standalone package for Linux desktop systems with NVIDIA GPUs.
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

def create_linux_package():
    """Create a Linux-compatible package."""
    
    print_step("Building Linux Package (x86_64)")
    
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / "dist" / "linux"
    
    # Clean up old builds
    if output_dir.exists():
        print("Cleaning up old build...")
        shutil.rmtree(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print_step("Creating Linux Package Structure")
    
    # Copy application source
    app_dir = output_dir / "TensorRT_Converter"
    app_src = app_dir / "src"
    app_dir.mkdir(exist_ok=True)
    
    print("Copying application files...")
    shutil.copytree(base_dir / "src", app_src)
    shutil.copy(base_dir / "main.py", app_dir / "main.py")
    
    # Create requirements for Linux
    linux_requirements = """# TensorRT Converter - Linux Requirements
# Install with: pip install -r requirements.txt

# GUI Framework
PyQt5>=5.15.0

# Deep Learning
torch>=2.0.0
torchvision>=0.15.0

# TensorRT (install from NVIDIA)
# Download from: https://developer.nvidia.com/tensorrt
# Or: pip install tensorrt (if available)
tensorrt>=8.6.0

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
    req_file.write_text(linux_requirements.strip())
    
    # Create launcher script
    launcher_content = """#!/bin/bash
# TensorRT Converter Launcher for Linux

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set Python path
export PYTHONPATH="$DIR:$DIR/src:$PYTHONPATH"

# Set LD_LIBRARY_PATH for TensorRT
if [ -d "/usr/local/tensorrt" ]; then
    export LD_LIBRARY_PATH="/usr/local/tensorrt/lib:$LD_LIBRARY_PATH"
fi

if [ -d "/usr/lib/x86_64-linux-gnu" ]; then
    export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
fi

# Check if running with GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo "⚠️  Warning: nvidia-smi not found. Make sure NVIDIA drivers are installed."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run the application
python3 "$DIR/main.py" "$@"
"""
    
    launcher_file = app_dir / "TensorRT_Converter.sh"
    launcher_file.write_text(launcher_content)
    
    # Create installation script
    install_script = """#!/bin/bash
# Installation script for TensorRT Converter on Linux

echo "======================================"
echo "  TensorRT Converter - Linux Setup"
echo "======================================"
echo ""

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo "❌ Cannot detect Linux distribution"
    exit 1
fi

echo "Detected: $PRETTY_NAME"
echo ""

# Check for NVIDIA GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo "⚠️  Warning: nvidia-smi not found"
    echo "Please install NVIDIA drivers first:"
    echo "  Ubuntu/Debian: sudo apt install nvidia-driver-525"
    echo "  Fedora: sudo dnf install akmod-nvidia"
    echo "  Arch: sudo pacman -S nvidia"
    read -p "Continue installation anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Step 1: Installing system dependencies..."

case $DISTRO in
    ubuntu|debian|linuxmint)
        sudo apt-get update
        sudo apt-get install -y \\
            python3 \\
            python3-pip \\
            python3-pyqt5 \\
            python3-venv \\
            libgl1-mesa-glx \\
            libglib2.0-0 \\
            libsm6 \\
            libxext6 \\
            libxrender-dev \\
            libgomp1
        ;;
    
    fedora|rhel|centos)
        sudo dnf install -y \\
            python3 \\
            python3-pip \\
            python3-qt5 \\
            mesa-libGL \\
            glib2 \\
            libSM \\
            libXext \\
            libXrender
        ;;
    
    arch|manjaro)
        sudo pacman -Syu --noconfirm \\
            python \\
            python-pip \\
            python-pyqt5 \\
            mesa \\
            glib2
        ;;
    
    *)
        echo "⚠️  Unsupported distribution: $DISTRO"
        echo "Please install Python3, PyQt5, and OpenGL libraries manually"
        ;;
esac

echo ""
echo "Step 2: Creating virtual environment..."
cd "$DIR"
python3 -m venv venv
source venv/bin/activate

echo ""
echo "Step 3: Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Step 4: Checking CUDA..."
python3 -c "import torch; print(f'PyTorch CUDA available: {torch.cuda.is_available()}')" || \\
    echo "⚠️  CUDA not available in PyTorch"

echo ""
echo "Step 5: Checking TensorRT..."
python3 -c "import tensorrt; print(f'TensorRT version: {tensorrt.__version__}')" 2>/dev/null || {
    echo "⚠️  TensorRT not found"
    echo ""
    echo "To install TensorRT:"
    echo "1. Download from: https://developer.nvidia.com/tensorrt"
    echo "2. Or try: pip install tensorrt"
    echo ""
}

echo ""
echo "Step 6: Setting up launcher..."
chmod +x TensorRT_Converter.sh

echo ""
echo "Step 7: Creating desktop entry..."
DESKTOP_FILE="$HOME/.local/share/applications/tensorrt-converter.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=TensorRT Converter
Comment=Convert models to TensorRT format
Exec=$DIR/TensorRT_Converter.sh
Icon=application-x-executable
Terminal=false
Categories=Development;Graphics;
EOF

echo ""
echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "To run the application:"
echo "  $DIR/TensorRT_Converter.sh"
echo ""
echo "Or search for 'TensorRT Converter' in your application menu"
echo ""
echo "⚠️  Note: Activate venv before running:"
echo "  source $DIR/venv/bin/activate"
echo "  python3 main.py"
echo ""
"""
    
    install_file = app_dir / "install.sh"
    install_file.write_text(install_script)
    
    # Create README for Linux
    readme_content = """# TensorRT Converter - Linux Edition

## Supported Systems

- ✅ Ubuntu 20.04+ / Debian 11+
- ✅ Fedora 35+ / RHEL 8+
- ✅ Arch Linux / Manjaro
- ✅ Any Linux with NVIDIA GPU and CUDA support

## Prerequisites

### 1. NVIDIA Drivers
```bash
# Ubuntu/Debian
sudo apt install nvidia-driver-525

# Fedora
sudo dnf install akmod-nvidia

# Arch
sudo pacman -S nvidia
```

### 2. CUDA Toolkit (Optional but recommended)
Download from: https://developer.nvidia.com/cuda-downloads

### 3. TensorRT
Download from: https://developer.nvidia.com/tensorrt

Or install via pip (if available for your system):
```bash
pip install tensorrt
```

## Installation

### Quick Install (Recommended)

```bash
tar -xzf TensorRT_Converter_Linux.tar.gz
cd TensorRT_Converter
chmod +x install.sh
./install.sh
```

### Manual Install

```bash
# Extract
tar -xzf TensorRT_Converter_Linux.tar.gz
cd TensorRT_Converter

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install python3 python3-pip python3-pyqt5 python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Make launcher executable
chmod +x TensorRT_Converter.sh
```

## Running the Application

### Option 1: Use the launcher
```bash
./TensorRT_Converter.sh
```

### Option 2: Run directly with Python
```bash
source venv/bin/activate
python3 main.py
```

### Option 3: From application menu
After installation, search for "TensorRT Converter" in your application menu.

## Configuration

### CUDA Paths
If CUDA is not in standard location, set environment variables:
```bash
export CUDA_HOME=/usr/local/cuda
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
export PATH=$CUDA_HOME/bin:$PATH
```

### TensorRT Paths
If TensorRT is not found:
```bash
export LD_LIBRARY_PATH=/path/to/tensorrt/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/path/to/tensorrt/python:$PYTHONPATH
```

## Troubleshooting

### "ImportError: libnvinfer.so.8"
TensorRT library not found. Solutions:
1. Install TensorRT: https://developer.nvidia.com/tensorrt
2. Set LD_LIBRARY_PATH to TensorRT lib directory
3. Create symbolic link: `sudo ln -s /path/to/libnvinfer.so.X /usr/lib/`

### "CUDA not available"
1. Check NVIDIA drivers: `nvidia-smi`
2. Verify CUDA installation: `nvcc --version`
3. Reinstall PyTorch with CUDA:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### "Cannot connect to X server"
For headless servers or remote access:
```bash
# Enable X11 forwarding in SSH
ssh -X user@host

# Or use VNC/Remote Desktop
```

### Permission denied
```bash
chmod +x TensorRT_Converter.sh
chmod +x install.sh
```

## Performance Optimization

### 1. Use Performance Mode
```bash
# Set CPU governor to performance
sudo cpupower frequency-set -g performance
```

### 2. Disable Desktop Effects
For better GPU performance during conversion.

### 3. Increase GPU Power Limit (if supported)
```bash
sudo nvidia-smi -pl 300  # Set to 300W (adjust for your GPU)
```

## Uninstallation

```bash
rm -rf ~/TensorRT_Converter
rm ~/.local/share/applications/tensorrt-converter.desktop
```

## Package Contents

```
TensorRT_Converter/
├── main.py                 # Main application
├── src/                    # Source code
├── requirements.txt        # Python dependencies
├── install.sh             # Installation script
├── TensorRT_Converter.sh  # Launcher script
└── README_LINUX.md        # This file
```

## Building from Source

If you want to modify the application:

```bash
# Install development dependencies
pip install -r requirements.txt

# Run directly
python3 main.py

# Or package with PyInstaller
pip install pyinstaller
pyinstaller main.spec
```

## Support

- GitHub Issues: [Your repo]
- NVIDIA Developer Forums: https://forums.developer.nvidia.com/
- TensorRT Documentation: https://docs.nvidia.com/deeplearning/tensorrt/

---
Tested on Ubuntu 22.04 LTS with NVIDIA RTX series GPUs
"""
    
    readme_file = app_dir / "README_LINUX.md"
    readme_file.write_text(readme_content)
    
    # Create version info
    version_info = {
        "app_name": "TensorRT Converter",
        "version": "1.0.0",
        "platform": "Linux x86_64",
        "build_date": "2025-10-22",
        "supported_distros": [
            "Ubuntu 20.04+",
            "Debian 11+",
            "Fedora 35+",
            "RHEL 8+",
            "Arch Linux"
        ],
        "requirements": {
            "nvidia_driver": "525.60+",
            "cuda": "11.8+ (recommended)",
            "tensorrt": "8.6.0+",
            "python": "3.8+"
        }
    }
    
    version_file = app_dir / "version_info.json"
    version_file.write_text(json.dumps(version_info, indent=2))
    
    print_step("Creating tarball package")
    
    # Create tarball
    import tarfile
    
    tarball_path = base_dir / "dist" / "TensorRT_Converter_Linux.tar.gz"
    
    print(f"Creating {tarball_path}...")
    with tarfile.open(tarball_path, "w:gz") as tar:
        tar.add(app_dir, arcname="TensorRT_Converter")
    
    size_mb = tarball_path.stat().st_size / (1024 * 1024)
    
    print_step("Build Complete!")
    
    print(f"""
✅ Successfully created Linux package!

📦 Package Details:
   - Location: {tarball_path}
   - Size: {size_mb:.1f} MB
   - Platform: Linux x86_64

📋 Installation on Linux:

   1. Extract the package:
      tar -xzf TensorRT_Converter_Linux.tar.gz
      cd TensorRT_Converter
   
   2. Run the installer:
      chmod +x install.sh
      ./install.sh
   
   3. Launch the application:
      ./TensorRT_Converter.sh

⚠️  Linux Requirements:
   - NVIDIA GPU with CUDA support
   - NVIDIA Drivers (525.60+)
   - CUDA Toolkit (11.8+ recommended)
   - TensorRT (8.6.0+)
   - Python 3.8+

📚 Documentation:
   - See README_LINUX.md in the package
   - Troubleshooting guide included

🐧 Tested on:
   - Ubuntu 22.04 LTS
   - Fedora 38
   - Arch Linux (2023)
""")
    
    return True

if __name__ == "__main__":
    try:
        if create_linux_package():
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
