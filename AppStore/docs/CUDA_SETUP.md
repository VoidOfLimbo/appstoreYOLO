# CUDA 13.0 Setup Guide

## 🎯 Overview

This guide explains how to set up AppStore with CUDA 13.0 for GPU acceleration.

## ✅ Current CUDA 13.0 Status

Your system is now configured with:
- ✅ **CUDA Toolkit 13.0** (V13.0.88) - Detected via `nvcc --version`
- ✅ **CuPy 13.6.0** - GPU array operations with CUDA 13.x
- ✅ **TensorRT 10.13.3.9** - Model optimization with CUDA 13 support
- ✅ **OpenCV 4.12.0** - Computer vision (CPU version with contrib modules)
- ✅ **NumPy 2.2.6** - CUDA-compatible version

## 📦 Installed Packages

### CUDA-Enabled Packages
```
cupy-cuda13x==13.6.0          # GPU acceleration for NumPy-like operations
tensorrt==10.13.3.9            # NVIDIA TensorRT for model inference
nvidia-cuda-runtime-cu13       # CUDA 13 runtime libraries
```

### Core Packages (CUDA Compatible)
```
numpy==2.2.6                   # Compatible with CUDA 13.0
opencv-contrib-python==4.12.0  # CPU version with extra modules
pyqt5==5.15.11                 # GUI framework
matplotlib==3.10.7             # Visualization
pillow==12.0.0                 # Image processing
pyinstaller==6.16.0            # Executable creation
```

## 🚀 GPU Acceleration Usage

### Using CuPy for GPU Operations

CuPy provides GPU-accelerated NumPy operations:

```python
import cupy as cp
import numpy as np

# Create array on GPU
gpu_array = cp.array([1, 2, 3, 4, 5])

# Perform GPU operations
result = cp.sum(gpu_array ** 2)

# Transfer back to CPU if needed
cpu_result = cp.asnumpy(result)
print(f"Result: {cpu_result}")
```

### Using TensorRT for Model Inference

TensorRT is now available for model optimization:

```python
import tensorrt as trt

# Create TensorRT logger
logger = trt.Logger(trt.Logger.WARNING)

# Build engine from ONNX
builder = trt.Builder(logger)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
parser = trt.OnnxParser(network, logger)

# Parse ONNX model and build engine
# ... (see TensorRT documentation for full example)
```

### OpenCV with CuPy Integration

While OpenCV isn't built with CUDA, you can use CuPy for GPU operations:

```python
import cv2
import cupy as cp

# Load image with OpenCV
image = cv2.imread('image.jpg')

# Convert to CuPy array for GPU processing
gpu_image = cp.asarray(image)

# Perform GPU operations
processed = cp.clip(gpu_image * 1.5, 0, 255).astype(cp.uint8)

# Convert back to NumPy for OpenCV
result = cp.asnumpy(processed)

# Save with OpenCV
cv2.imwrite('output.jpg', result)
```

## 🔍 Verification

Run the verification script to check your setup:

```bash
python verify_cuda.py
```

Expected output:
```
✓ CUDA 13.0 support is available via CuPy and TensorRT
✓ GPU available: True
✓ NVCC installed: Cuda compilation tools, release 13.0
```

## 📊 Performance Comparison

### CPU vs GPU Operations

```python
import numpy as np
import cupy as cp
import time

size = 10000

# CPU benchmark
cpu_array = np.random.rand(size, size)
start = time.time()
cpu_result = np.dot(cpu_array, cpu_array)
cpu_time = time.time() - start

# GPU benchmark
gpu_array = cp.random.rand(size, size)
start = time.time()
gpu_result = cp.dot(gpu_array, gpu_array)
cp.cuda.Stream.null.synchronize()
gpu_time = time.time() - start

print(f"CPU time: {cpu_time:.4f}s")
print(f"GPU time: {gpu_time:.4f}s")
print(f"Speedup: {cpu_time/gpu_time:.2f}x")
```

## 🔧 Building OpenCV with CUDA (Optional)

If you need OpenCV with full CUDA support, you'll need to build from source:

### Prerequisites
1. CUDA Toolkit 13.0 (already installed ✓)
2. CMake (3.20+)
3. Visual Studio 2019/2022 with C++ tools

### Build Steps (Advanced)

```bash
# Clone OpenCV and contrib modules
git clone https://github.com/opencv/opencv.git
git clone https://github.com/opencv/opencv_contrib.git

# Create build directory
mkdir opencv_build
cd opencv_build

# Configure with CMake
cmake -D CMAKE_BUILD_TYPE=RELEASE ^
      -D CMAKE_INSTALL_PREFIX=install ^
      -D WITH_CUDA=ON ^
      -D CUDA_TOOLKIT_ROOT_DIR="C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.0" ^
      -D WITH_CUDNN=ON ^
      -D OPENCV_DNN_CUDA=ON ^
      -D ENABLE_FAST_MATH=ON ^
      -D CUDA_FAST_MATH=ON ^
      -D CUDA_ARCH_BIN=7.5,8.0,8.6,8.9,9.0 ^
      -D WITH_CUBLAS=ON ^
      -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules ^
      -D BUILD_EXAMPLES=OFF ^
      ../opencv

# Build (takes 30-60 minutes)
cmake --build . --config Release --target INSTALL

# Install the built package
pip install install/python
```

**Note:** Building OpenCV with CUDA is complex and time-consuming. For most use cases, CuPy provides sufficient GPU acceleration.

## 🎯 Recommended Approach

For **AppStore** applications:

1. **Use TensorRT** for model inference (✓ Already installed)
2. **Use CuPy** for GPU array operations (✓ Already installed)
3. **Use OpenCV** for image I/O and preprocessing (CPU is fine for this)
4. **Use GPU** for heavy computations (via CuPy/TensorRT)

This hybrid approach gives you:
- ✅ Easy installation (no compilation)
- ✅ GPU acceleration where it matters
- ✅ Reliable OpenCV functionality
- ✅ Full CUDA 13.0 support

## 🐛 Troubleshooting

### CuPy Import Errors
```bash
# Ensure CUDA is in PATH
set PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.0\bin;%PATH%

# Verify CUDA runtime
python -c "import cupy as cp; print(cp.cuda.runtime.runtimeGetVersion())"
```

### TensorRT Not Found
```bash
# Reinstall TensorRT
pip uninstall tensorrt
pip install tensorrt --no-cache-dir
```

### GPU Not Detected
```bash
# Check NVIDIA driver
nvidia-smi

# Verify CUDA devices
python -c "import cupy as cp; print(f'GPU available: {cp.cuda.is_available()}')"
```

## 📈 Performance Tips

1. **Keep data on GPU** - Minimize CPU↔GPU transfers
2. **Use batch operations** - Process multiple items together
3. **Profile your code** - Use CuPy's profiler to find bottlenecks
4. **Use TensorRT** - 2-10x faster inference than standard frameworks

## 🎉 Success!

Your system is now configured for CUDA 13.0 acceleration:
- ✅ TensorRT for model optimization
- ✅ CuPy for GPU array operations
- ✅ Compatible with all existing code
- ✅ Ready for production deployment

Run `python verify_cuda.py` to confirm everything is working!

---

**Note:** The warning about TensorRT not being installed should now be gone when you run the application!
