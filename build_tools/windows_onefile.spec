# -*- mode: python ; coding: utf-8 -*-

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
