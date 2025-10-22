"""
PyInstaller hook for ultralytics to include all necessary modules.
"""
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Collect all ultralytics submodules
hiddenimports = collect_submodules('ultralytics')

# Add specific modules that might be missed
hiddenimports += [
    'ultralytics.cfg',
    'ultralytics.data',
    'ultralytics.engine',
    'ultralytics.models',
    'ultralytics.nn',
    'ultralytics.trackers',
    'ultralytics.utils',
    'ultralytics.models.yolo',
]

# Collect data files (configs, default models, etc.)
datas = collect_data_files('ultralytics', include_py_files=True)
