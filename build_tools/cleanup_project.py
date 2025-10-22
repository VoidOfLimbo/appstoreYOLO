"""
Project cleanup and reorganization script.
Moves unnecessary files to archive and organizes the project structure.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def print_step(message):
    """Print a step message."""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")

def cleanup_project():
    """Clean up and reorganize the project."""
    
    print_step("TensorRT Converter - Project Cleanup")
    
    base_dir = Path(__file__).parent.parent
    
    # Create archive directory
    archive_dir = base_dir / "archive" / datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Archive directory: {archive_dir}")
    
    # Files and directories to archive (no longer needed)
    to_archive = [
        "build_exe.py",  # Old build script
        "create_portable.py",  # Old portable builder
        "create_standalone_installer.py",  # Old installer builder
        "check_cuda.py",  # Testing script
        "test_system.py",  # Testing script
        "tensorrt_converter.spec",  # Old PyInstaller spec
        "hook-onnx.py",  # PyInstaller hook (moved to hooks/)
        "python_embedded.zip",  # Downloaded Python
        "get-pip.py",  # Downloaded pip installer
        "embedded_requirements.txt",  # Old requirements
        "portable_package/",  # Old portable build
        "portable_env/",  # Old portable environment
        "build/",  # PyInstaller build artifacts
        "installer_output/",  # Inno Setup output
        "__pycache__/",  # Python cache
        "src/__pycache__/",
        "src/gui/__pycache__/",
        "src/utils/__pycache__/",
    ]
    
    # Documentation files to move to docs/
    docs_files = [
        "QUICKSTART.md",
        "TROUBLESHOOTING.md",
        "CUDA_SETUP_GUIDE.md",
        "PYINSTALLER_BUILD_GUIDE.md",
        "STANDALONE_INSTALLER_GUIDE.md",
        "DEPLOYMENT_READY.md",
        "DEVELOPMENT_GUIDE.md",
    ]
    
    # Configuration files to move to config/
    config_files = [
        "installer_config.iss",
        "LICENSE.txt",
    ]
    
    print_step("Step 1: Archiving old build files")
    
    archived_count = 0
    for item in to_archive:
        item_path = base_dir / item
        if item_path.exists():
            try:
                dest = archive_dir / item
                if item_path.is_dir():
                    shutil.move(str(item_path), str(dest))
                    print(f"  📦 Archived directory: {item}")
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(item_path), str(dest))
                    print(f"  📄 Archived file: {item}")
                archived_count += 1
            except Exception as e:
                print(f"  ⚠️  Could not archive {item}: {e}")
    
    print(f"\n  ✅ Archived {archived_count} items")
    
    print_step("Step 2: Organizing documentation")
    
    docs_dir = base_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    moved_docs = 0
    for doc in docs_files:
        doc_path = base_dir / doc
        if doc_path.exists():
            try:
                shutil.move(str(doc_path), str(docs_dir / doc))
                print(f"  📚 Moved: {doc}")
                moved_docs += 1
            except Exception as e:
                print(f"  ⚠️  Could not move {doc}: {e}")
    
    print(f"\n  ✅ Moved {moved_docs} documentation files to docs/")
    
    print_step("Step 3: Organizing configuration files")
    
    config_dir = base_dir / "config"
    config_dir.mkdir(exist_ok=True)
    
    moved_config = 0
    for cfg in config_files:
        cfg_path = base_dir / cfg
        if cfg_path.exists():
            try:
                shutil.move(str(cfg_path), str(config_dir / cfg))
                print(f"  ⚙️  Moved: {cfg}")
                moved_config += 1
            except Exception as e:
                print(f"  ⚠️  Could not move {cfg}: {e}")
    
    print(f"\n  ✅ Moved {moved_config} configuration files to config/")
    
    print_step("Step 4: Moving PyInstaller hooks")
    
    hooks_dir = base_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    
    # Check if hook-onnx.py exists in root (might be archived already)
    hook_file = base_dir / "hook-onnx.py"
    if hook_file.exists():
        shutil.move(str(hook_file), str(hooks_dir / "hook-onnx.py"))
        print(f"  🪝 Moved: hook-onnx.py to hooks/")
    
    print_step("Step 5: Cleaning up output directories")
    
    # Keep dist/ but clean old PyInstaller output
    dist_tensorrt = base_dir / "dist" / "TensorRT_Converter"
    if dist_tensorrt.exists():
        try:
            shutil.move(str(dist_tensorrt), str(archive_dir / "dist_TensorRT_Converter"))
            print(f"  📦 Archived: dist/TensorRT_Converter/ (old PyInstaller build)")
        except Exception as e:
            print(f"  ⚠️  Could not archive dist/TensorRT_Converter: {e}")
    
    # Clean __pycache__ recursively
    print("\n  🧹 Cleaning __pycache__ directories...")
    pycache_count = 0
    for pycache in base_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
            pycache_count += 1
        except:
            pass
    print(f"  ✅ Cleaned {pycache_count} __pycache__ directories")
    
    # Clean .pyc files
    print("\n  🧹 Cleaning .pyc files...")
    pyc_count = 0
    for pyc in base_dir.rglob("*.pyc"):
        try:
            pyc.unlink()
            pyc_count += 1
        except:
            pass
    print(f"  ✅ Cleaned {pyc_count} .pyc files")
    
    print_step("Step 6: Creating project structure summary")
    
    # Create a structure file
    structure_file = base_dir / "PROJECT_STRUCTURE.md"
    structure_content = """# TensorRT Converter - Project Structure

## Root Directory

```
TensorRT_Converter/
├── main.py                     # Application entry point
├── README.md                   # Main documentation
├── requirements.txt            # Python dependencies
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── gui/                   # GUI components
│   │   ├── __init__.py
│   │   └── main_window.py    # Main window and UI
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       ├── hardware_detector.py
│       ├── tensorrt_converter.py
│       └── logger.py
│
├── build_tools/               # Build scripts for all platforms
│   ├── build_all.py          # Master build script
│   ├── build_windows_exe.py  # Windows executable builder
│   ├── build_linux.py        # Linux package builder
│   ├── build_jetson.py       # Jetson package builder
│   └── windows_onefile.spec  # PyInstaller spec (generated)
│
├── docs/                      # Documentation
│   ├── QUICKSTART.md
│   ├── TROUBLESHOOTING.md
│   ├── CUDA_SETUP_GUIDE.md
│   ├── PYINSTALLER_BUILD_GUIDE.md
│   ├── STANDALONE_INSTALLER_GUIDE.md
│   ├── DEPLOYMENT_READY.md
│   └── DEVELOPMENT_GUIDE.md
│
├── config/                    # Configuration files
│   ├── installer_config.iss  # Inno Setup configuration
│   └── LICENSE.txt           # License file
│
├── hooks/                     # PyInstaller hooks
│   └── hook-onnx.py          # ONNX module hook
│
├── assets/                    # Assets (icons, images)
│   └── icon.ico              # Application icon (if exists)
│
├── dist/                      # Build output
│   ├── windows/              # Windows builds
│   ├── linux/                # Linux builds
│   ├── jetson/               # Jetson builds
│   ├── TensorRT_Converter_Windows.exe
│   ├── TensorRT_Converter_Linux.tar.gz
│   └── TensorRT_Converter_Jetson.tar.gz
│
├── logs/                      # Application logs (runtime)
├── output/                    # Converted models (runtime)
│
└── archive/                   # Archived old files
    └── YYYYMMDD_HHMMSS/      # Timestamped archive
```

## Key Files

### Application
- **main.py**: Entry point, initializes and runs the GUI
- **src/gui/main_window.py**: Main PyQt5 GUI with drag-drop, hardware detection, conversion
- **src/utils/tensorrt_converter.py**: Core TensorRT conversion logic
- **src/utils/hardware_detector.py**: GPU/CUDA/TensorRT detection
- **src/config.py**: Application configuration and constants

### Build Tools
- **build_tools/build_all.py**: Interactive builder for all platforms
- **build_tools/build_windows_exe.py**: Creates single-file Windows .exe
- **build_tools/build_linux.py**: Creates Linux x86_64 package
- **build_tools/build_jetson.py**: Creates ARM64 Jetson package

### Documentation
- **README.md**: Main project documentation and usage
- **docs/QUICKSTART.md**: Quick start guide
- **docs/TROUBLESHOOTING.md**: Common issues and solutions
- **docs/CUDA_SETUP_GUIDE.md**: CUDA installation guide
- **docs/DEPLOYMENT_READY.md**: Deployment instructions

## Build Outputs

### Windows
- **Single-file executable**: `dist/windows/TensorRT_Converter_Windows.exe`
- Size: ~500MB - 1GB (includes Python + PyTorch + TensorRT)
- Target: Windows 10/11 64-bit with NVIDIA GPU

### Linux
- **Tarball package**: `dist/TensorRT_Converter_Linux.tar.gz`
- Size: ~10MB (source + scripts)
- Requires: Python installation on target system
- Target: Ubuntu/Debian/Fedora/Arch with NVIDIA GPU

### Jetson
- **Tarball package**: `dist/TensorRT_Converter_Jetson.tar.gz`
- Size: ~10MB (source + scripts)
- Requires: JetPack installed on Jetson device
- Target: Jetson Nano/TX2/Xavier/Orin

## Development Workflow

1. **Edit source code**: Modify files in `src/`
2. **Test locally**: Run `python main.py`
3. **Build for platform**: Run `python build_tools/build_all.py`
4. **Test build**: Test the output in `dist/`
5. **Deploy**: Distribute the platform-specific package

## Clean Project Structure

The following directories are auto-generated and can be deleted:
- `__pycache__/` - Python cache
- `build/` - PyInstaller temporary build files
- `logs/` - Runtime application logs
- `output/` - Converted model outputs

These will be recreated automatically when needed.

---
Last updated: October 22, 2025
"""
    
    structure_file.write_text(structure_content, encoding='utf-8')
    print(f"  Created: PROJECT_STRUCTURE.md")
    
    print_step("Cleanup Complete!")
    
    print(f"""
✅ Project successfully reorganized!

📂 New structure:
   Root (clean):
   - main.py
   - README.md
   - requirements.txt
   - PROJECT_STRUCTURE.md

   Organized directories:
   - src/              (source code)
   - build_tools/      (platform builders)
   - docs/             (documentation)
   - config/           (configuration files)
   - hooks/            (PyInstaller hooks)
   - dist/             (build outputs)
   - archive/          (old files)

📦 Archived items:
   {archived_count} files/directories moved to:
   {archive_dir}

📚 Documentation:
   {moved_docs} files organized in docs/

⚙️  Configuration:
   {moved_config} files organized in config/

🧹 Cleaned:
   - {pycache_count} __pycache__ directories
   - {pyc_count} .pyc files

🎯 Next steps:
   1. Review the new structure
   2. Test the application: python main.py
   3. Build for platforms: python build_tools/build_all.py
   4. Delete archive/ folder if everything works

⚠️  Note: You can safely delete the archive/ folder after
   verifying everything works correctly.
""")
    
    return True

if __name__ == "__main__":
    try:
        if cleanup_project():
            print("\n✅ SUCCESS: Project cleanup completed!\n")
        else:
            print("\n❌ ERROR: Project cleanup failed\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
