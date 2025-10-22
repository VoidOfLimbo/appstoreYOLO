"""
PyInstaller hook for TensorRT to include necessary DLLs.
"""
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files
import os
import sys

# Collect TensorRT binaries
binaries = collect_dynamic_libs('tensorrt')
binaries += collect_dynamic_libs('tensorrt_bindings')

# Add CUDA and TensorRT DLL paths
# These should be in the system PATH
cuda_paths = []
for path in os.environ.get('PATH', '').split(os.pathsep):
    if 'CUDA' in path.upper() or 'TensorRT' in path:
        cuda_paths.append(path)

# Look for TensorRT DLLs
tensorrt_dlls = [
    'nvinfer_10.dll',
    'nvinfer_plugin_10.dll',
    'nvonnxparser_10.dll',
    'nvinfer_dispatch_10.dll',
    'nvinfer_lean_10.dll',
]

# Try to find and include TensorRT DLLs
for dll_name in tensorrt_dlls:
    for cuda_path in cuda_paths:
        dll_path = os.path.join(cuda_path, dll_name)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))
            break

# Collect data files
datas = collect_data_files('tensorrt', include_py_files=False)
datas += collect_data_files('tensorrt_bindings', include_py_files=False)

hiddenimports = [
    'tensorrt',
    'tensorrt_bindings',
]
