"""
PyInstaller hook for onnxruntime to include TensorRT provider DLLs.
"""
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_data_files
import os

# Collect onnxruntime binaries
binaries = collect_dynamic_libs('onnxruntime')

# Look for TensorRT provider DLLs
cuda_paths = []
for path in os.environ.get('PATH', '').split(os.pathsep):
    if 'CUDA' in path.upper() or 'TensorRT' in path:
        cuda_paths.append(path)

# TensorRT provider dependencies
tensorrt_provider_dlls = [
    'nvinfer_10.dll',
    'nvinfer_plugin_10.dll',
    'nvonnxparser_10.dll',
]

for dll_name in tensorrt_provider_dlls:
    for cuda_path in cuda_paths:
        dll_path = os.path.join(cuda_path, dll_name)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))
            break

datas = collect_data_files('onnxruntime', include_py_files=False)

hiddenimports = [
    'onnxruntime',
    'onnxruntime.capi',
    'onnxruntime.capi.onnxruntime_pybind11_state',
]
