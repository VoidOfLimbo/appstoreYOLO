"""
Runtime hook to add CUDA and TensorRT DLL paths to the system PATH.
This ensures TensorRT DLLs can be found at runtime.
"""
import os
import sys

# Add common CUDA/TensorRT paths to PATH
cuda_paths = [
    r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4\bin',
    r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3\bin',
    r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.2\bin',
    r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin',
    r'C:\Program Files\NVIDIA\TensorRT\v10\bin',
    r'C:\Program Files\NVIDIA\TensorRT\v9\bin',
    r'C:\Program Files\NVIDIA\TensorRT\v8\bin',
]

# Add existing CUDA paths from environment
for path in os.environ.get('PATH', '').split(os.pathsep):
    if 'CUDA' in path.upper() or 'TensorRT' in path.upper():
        if path not in cuda_paths:
            cuda_paths.insert(0, path)

# Add paths that exist
for cuda_path in cuda_paths:
    if os.path.exists(cuda_path):
        if cuda_path not in os.environ['PATH']:
            os.environ['PATH'] = cuda_path + os.pathsep + os.environ['PATH']
