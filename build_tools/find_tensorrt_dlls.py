"""
Helper script to find and copy TensorRT DLLs for PyInstaller.
This resolves the "Library not found" warnings.
"""
import os
import shutil
from pathlib import Path

def find_tensorrt_dlls():
    """Find TensorRT DLLs in the system."""
    required_dlls = [
        'nvinfer_10.dll',
        'nvinfer_plugin_10.dll',
        'nvonnxparser_10.dll',
        'nvinfer_dispatch_10.dll',
        'nvinfer_lean_10.dll',
        'nvinfer_builder_resource_10.dll',
    ]
    
    found_dlls = {}
    
    # First, search in Python site-packages (tensorrt_libs, onnxruntime)
    try:
        import site
        for site_dir in site.getsitepackages():
            site_path = Path(site_dir)
            
            # Check tensorrt_libs directory
            tensorrt_libs = site_path / 'tensorrt_libs'
            if tensorrt_libs.exists():
                for dll in required_dlls:
                    dll_path = tensorrt_libs / dll
                    if dll_path.exists() and dll not in found_dlls:
                        found_dlls[dll] = dll_path
            
            # Check onnxruntime capi directory
            onnx_capi = site_path / 'onnxruntime' / 'capi'
            if onnx_capi.exists():
                for dll in required_dlls:
                    dll_path = onnx_capi / dll
                    if dll_path.exists() and dll not in found_dlls:
                        found_dlls[dll] = dll_path
    except:
        pass
    
    # Search in PATH
    for path in os.environ.get('PATH', '').split(os.pathsep):
        if not os.path.exists(path):
            continue
            
        for dll in required_dlls:
            dll_path = Path(path) / dll
            if dll_path.exists() and dll not in found_dlls:
                found_dlls[dll] = dll_path
    
    # Search in common CUDA/TensorRT locations
    common_paths = [
        Path(r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4\bin'),
        Path(r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.3\bin'),
        Path(r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.2\bin'),
        Path(r'C:\Program Files\NVIDIA\TensorRT\v10\bin'),
        Path(r'C:\Program Files\NVIDIA\TensorRT\v9\bin'),
        Path(r'C:\Program Files\NVIDIA\TensorRT\v8\bin'),
    ]
    
    for common_path in common_paths:
        if not common_path.exists():
            continue
            
        for dll in required_dlls:
            dll_path = common_path / dll
            if dll_path.exists() and dll not in found_dlls:
                found_dlls[dll] = dll_path
    
    return found_dlls

def copy_tensorrt_dlls(dest_dir):
    """Copy TensorRT DLLs to a destination directory."""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    found_dlls = find_tensorrt_dlls()
    
    print("\nTensorRT DLL Status:")
    print("-" * 60)
    
    copied = []
    missing = []
    
    required_dlls = [
        'nvinfer_10.dll',
        'nvinfer_plugin_10.dll',
        'nvonnxparser_10.dll',
    ]
    
    for dll in required_dlls:
        if dll in found_dlls:
            src = found_dlls[dll]
            dst = dest_dir / dll
            shutil.copy2(src, dst)
            copied.append(dll)
            print(f"✓ {dll}: {src}")
        else:
            missing.append(dll)
            print(f"✗ {dll}: NOT FOUND")
    
    print("-" * 60)
    print(f"Copied {len(copied)} DLLs to {dest_dir}")
    
    if missing:
        print(f"\n⚠️  Warning: {len(missing)} DLLs not found:")
        for dll in missing:
            print(f"   - {dll}")
        print("\nThe executable may not work on systems without TensorRT installed.")
    
    return copied, missing

if __name__ == "__main__":
    # Copy to a temp directory for PyInstaller to pick up
    base_dir = Path(__file__).parent.parent
    dll_dir = base_dir / "build_tools" / "tensorrt_dlls"
    
    copied, missing = copy_tensorrt_dlls(dll_dir)
    
    if missing:
        print("\n💡 To fix missing DLLs:")
        print("   1. Ensure TensorRT is installed")
        print("   2. Add TensorRT bin directory to system PATH")
        print("   3. Restart this script")
