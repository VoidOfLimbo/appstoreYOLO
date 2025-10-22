"""
Build a true single-file executable for Windows using PyInstaller with embedded packages.
This creates ONE .exe file that includes everything.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_step(message):
    """Print a step message."""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")

def create_windows_executable():
    """Create a single-file Windows executable."""
    
    print_step("Building Single-File Windows Executable")
    
    base_dir = Path(__file__).parent.parent
    spec_file = base_dir / "build_tools" / "windows_onefile.spec"
    
    # Clear PyInstaller cache and build directories
    print_step("Clearing Build Cache")
    
    # Clear PyInstaller cache
    venv_path = base_dir / ".venv"
    pyinstaller_cache = venv_path / "Lib" / "site-packages" / "PyInstaller" / "cache"
    
    if pyinstaller_cache.exists():
        print(f"Removing PyInstaller cache: {pyinstaller_cache}")
        shutil.rmtree(pyinstaller_cache, ignore_errors=True)
        print("✓ PyInstaller cache cleared")
    
    # Clear build directory
    build_dir = base_dir / "build"
    if build_dir.exists():
        print(f"Removing build directory: {build_dir}")
        shutil.rmtree(build_dir, ignore_errors=True)
        print("✓ Build directory cleared")
    
    # Clear dist directory
    dist_dir = base_dir / "dist" / "windows"
    if dist_dir.exists():
        print(f"Removing dist directory: {dist_dir}")
        shutil.rmtree(dist_dir, ignore_errors=True)
        print("✓ Dist directory cleared")
    
    print("All caches cleared successfully!")
    
    # Find and copy TensorRT DLLs
    print_step("Finding TensorRT DLLs")
    dll_finder = base_dir / "build_tools" / "find_tensorrt_dlls.py"
    subprocess.run([sys.executable, str(dll_finder)], cwd=base_dir)
    
    # Create optimized spec file for single-file build
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os
from pathlib import Path

# Get the base directory (current working directory when PyInstaller runs)
base_dir = Path(os.getcwd())

# Prepare TensorRT DLLs
tensorrt_dll_dir = base_dir / 'build_tools' / 'tensorrt_dlls'
tensorrt_binaries = []
if tensorrt_dll_dir.exists():
    for dll in tensorrt_dll_dir.glob('*.dll'):
        tensorrt_binaries.append((str(dll), '.'))

# Prepare paths
hooks_dir = str(base_dir / 'hooks')
runtime_hook = str(base_dir / 'hooks' / 'rthook_tensorrt.py')

a = Analysis(
    [str(base_dir / 'main.py')],
    pathex=[str(base_dir / 'src')],
    binaries=tensorrt_binaries,
    datas=[
        (str(base_dir / 'src'), 'src'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.sip',
        'torch._C',
        'torch._VF',
        'torch.nn',
        'torch.cuda',
        'torch.jit',
        'torch.onnx',
        'torchvision',
        'tensorrt',
        'tensorrt_bindings',
        'onnx',
        'onnxruntime',
        'onnxruntime.capi',
        'onnxslim',
        'cv2',
        'PIL',
        'numpy',
        'psutil',
        'ultralytics',
        'ultralytics.cfg',
        'ultralytics.engine',
        'ultralytics.models',
        'ultralytics.nn',
        'cpuinfo',
    ],
    hookspath=[hooks_dir],
    hooksconfig={},
    runtime_hooks=[runtime_hook],
    excludes=[
        # Exclude modules that cause warnings
        'tensorboard',
        'torch.utils.tensorboard',
        'torch.distributed.elastic',
        'torch.distributed._sharding_spec',
        'torch.distributed._sharded_tensor',
        'torch.testing',
        'torch.profiler',
        'torch.quantization',
        # Exclude unused large modules
        'matplotlib',
        'scipy',
        'pandas',
        'IPython',
        'jupyter',
        'notebook',
        'tkinter',
        'test',
        'tests',
        'onnx.reference',
        'onnx.reference.ops',
        # Exclude PyQt5 modules we don't need
        'PyQt5.QtBluetooth',
        'PyQt5.QtDBus',
        'PyQt5.QtDesigner',
        'PyQt5.QtNetwork',
        'PyQt5.QtWebEngine',
        'PyQt5.QtWebEngineCore',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebSockets',
        'PyQt5.QtXml',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    module_collection_mode={
        'onnx': 'py',
    }
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TensorRT_Converter_Windows',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
"""
    
    print("Creating spec file...")
    spec_file.write_text(spec_content)
    
    print_step("Running PyInstaller (This will take 10-15 minutes)")
    print("Building single-file executable with UPX compression...")
    print("Note: TensorRT and PyTorch are large, final .exe will be 500MB-1GB")
    
    # Find the venv python
    venv_python = base_dir / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        print(f"❌ ERROR: Virtual environment not found at {venv_python}")
        print("Please ensure .venv is created and PyInstaller is installed:")
        print("  python -m venv .venv")
        print("  .venv\\Scripts\\activate")
        print("  pip install pyinstaller")
        return False
    
    cmd = [
        str(venv_python),
        "-m", "PyInstaller",
        str(spec_file),
        "--clean",
        "--log-level=WARN",
        "--distpath", str(base_dir / "dist" / "windows"),
    ]
    
    result = subprocess.run(cmd, cwd=base_dir)
    
    if result.returncode == 0:
        print_step("Build Complete!")
        
        exe_path = base_dir / "dist" / "windows" / "TensorRT_Converter_Windows.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"""
✅ Successfully created Windows executable!

📦 File Details:
   - Location: {exe_path}
   - Size: {size_mb:.1f} MB
   - Type: Single-file executable

⚠️  Important Notes:
   - First run will extract to temp folder (slower startup)
   - Subsequent runs will be faster
   - Antivirus may flag large executables (false positive)
   - Target PC still needs NVIDIA drivers + GPU

🚀 To Use:
   1. Copy TensorRT_Converter_Windows.exe to target PC
   2. Double-click to run
   3. That's it!

📋 Target PC Requirements:
   - Windows 10/11 (64-bit)
   - NVIDIA GPU with CUDA support
   - NVIDIA Drivers (525.60+)
""")
            return True
        else:
            print("❌ ERROR: Executable not found after build")
            return False
    else:
        print("❌ ERROR: Build failed")
        return False

if __name__ == "__main__":
    try:
        if create_windows_executable():
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
