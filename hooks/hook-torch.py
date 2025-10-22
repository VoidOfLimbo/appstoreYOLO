"""
PyInstaller hook for torch to exclude unnecessary modules and fix warnings.
"""
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect necessary torch modules
hiddenimports = [
    'torch._C',
    'torch._VF',
    'torch.nn',
    'torch.optim',
    'torch.autograd',
    'torch.cuda',
    'torch.jit',
    'torch.onnx',
    'torch.utils',
    'torch.utils.data',
]

# Exclude unnecessary modules to reduce size
excludedimports = [
    'torch.utils.tensorboard',  # Not needed, causes tensorboard warning
    'torch.distributed.elastic',  # Not needed for conversion
    'torch.testing',
    'torch.profiler',
    'torch.quantization',
    'torch.distributed._sharding_spec',  # Deprecated module
    'torch.distributed._sharded_tensor',  # Deprecated module
]

# Collect data files
datas = collect_data_files('torch', include_py_files=False)
