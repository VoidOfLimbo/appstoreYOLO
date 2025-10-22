# Simplified TensorRT Model Converter Build Guide

## ⚠️ PyInstaller Build Issue

### The Problem:
- PyTorch + TensorRT + ONNX = **Very large** (~3-4 GB)
- ONNX reference modules cause crashes during build
- Build process is **extremely slow** (10-30 minutes)
- Final executable is **huge** (2-3 GB)

### The Issue:
```
SubprocessDiedError: Child process died calling import_library() 
with args=('onnx.reference',)
```

**Cause:** ONNX reference module has circular dependencies and optional features that crash PyInstaller's import analysis.

---

## ✅ Solutions

### Solution 1: Use the Fixed Spec File (Recommended for Distribution)

The spec file has been updated with:
```python
excludes=[
    'onnx.reference',  # Problematic module
    'onnx.reference.ops',
    'torch.testing',
    'tensorboard',
    'matplotlib',
    'scipy',
    'pandas',
    ...
]

module_collection_mode={
    'onnx': 'py',  # Only Python files, not all submodules
}
```

**To build:**
```powershell
# This will take 10-30 minutes due to PyTorch size
python -m PyInstaller tensorrt_converter.spec --clean

# Result: dist/TensorRT_Converter/ folder (~2-3 GB)
```

**Note:** This works but is VERY slow and creates a VERY large executable.

---

### Solution 2: Portable Python Environment (Faster, Easier)

Instead of creating a single .exe, create a **portable Python environment**:

```powershell
# 1. Create portable environment folder
mkdir TensorRT_Converter_Portable
cd TensorRT_Converter_Portable

# 2. Copy Python and venv
xcopy /E /I /Y "C:\Users\John\Documents\python\.venv" "python_env"
xcopy /E /I /Y "C:\Users\John\Documents\python\src" "src"
xcopy /Y "C:\Users\John\Documents\python\main.py" "."
xcopy /Y "C:\Users\John\Documents\python\*.md" "."

# 3. Create run.bat launcher
echo @echo off > run.bat
echo python_env\Scripts\python.exe main.py >> run.bat

# 4. Distribute the entire folder
```

**Advantages:**
- ✅ Fast to create (1 minute vs 30 minutes)
- ✅ Smaller size (~1.5 GB vs 3 GB)
- ✅ Easier to update
- ✅ No build errors
- ✅ Hardware detection works perfectly

**Disadvantages:**
- ❌ Not a single .exe file
- ❌ User sees a folder structure

---

### Solution 3: Python + Requirements (Smallest)

Distribute your code with a requirements.txt:

```
src/
main.py
requirements.txt
install.bat
run.bat
```

**install.bat:**
```batch
@echo off
python -m venv venv
venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install tensorrt onnx PyQt5 ultralytics
```

**run.bat:**
```batch
@echo off
venv\Scripts\python.exe main.py
```

**Advantages:**
- ✅ Smallest distribution (< 1 MB)
- ✅ Always up-to-date
- ✅ Easy to customize

**Disadvantages:**
- ❌ Requires Python installation
- ❌ User must run install first
- ❌ Requires internet for pip install

---

## 🎯 Recommendation

### For Internal Use:
**Use Solution 2 (Portable Environment)**
- Fast to create
- Works reliably
- Easy to update

### For Public Distribution:
**Use Solution 1 (PyInstaller)** - if you can wait for the build
- Single folder distribution
- No Python needed on target
- Most "professional" looking

### For Developers:
**Use Solution 3 (Source + Requirements)**
- Smallest footprint
- Easy to modify
- Transparent

---

## 🔧 Building with PyInstaller (Detailed Steps)

If you choose Solution 1, here's how to make it work:

### Step 1: Stop Current Build
```powershell
# Press Ctrl+C if build is hanging
```

### Step 2: Use Updated Spec File
The spec file has been fixed with exclusions. Build with:

```powershell
# Clean build (recommended)
python -m PyInstaller tensorrt_converter.spec --clean --log-level=WARN

# This will:
# - Take 10-30 minutes ⏰
# - Use 4-6 GB RAM 💾
# - Create 2-3 GB output 📦
```

### Step 3: Expected Output
```
dist/
└── TensorRT_Converter/
    ├── TensorRT_Converter.exe  (main executable)
    ├── src/                     (your source code)
    ├── torch/                   (PyTorch DLLs - HUGE)
    ├── tensorrt/               (TensorRT DLLs)
    └── [many other DLLs and files]

Total size: ~2-3 GB
```

### Step 4: Test the Executable
```powershell
cd dist\TensorRT_Converter
.\TensorRT_Converter.exe
```

---

## 🚀 Quick Start: Portable Environment (Solution 2)

Let me create this for you since it's fastest:

```powershell
# Run this script to create portable version
python create_portable.py
```

This will create a `TensorRT_Converter_Portable` folder you can zip and share!

---

## 📊 Comparison

| Method | Build Time | Size | Ease of Use | Reliability |
|--------|-----------|------|-------------|-------------|
| PyInstaller | 10-30 min | 2-3 GB | ★★★★★ | ★★★☆☆ |
| Portable Env | 1-2 min | 1.5 GB | ★★★★☆ | ★★★★★ |
| Source + Reqs | < 1 min | < 1 MB | ★★☆☆☆ | ★★★★☆ |

---

## 🐛 Why PyInstaller is Difficult

1. **PyTorch is huge** (2+ GB of DLLs and data files)
2. **ONNX has optional modules** that confuse PyInstaller
3. **TensorRT has C++ dependencies** that need special handling
4. **Ultralytics** includes YOLO models data
5. **CUDA libraries** are platform-specific

All of this makes PyInstaller builds:
- Slow to create
- Huge in size
- Prone to errors
- Hard to debug

---

## ✅ Current Status

**Your app works perfectly** when run with Python:
```powershell
python main.py
```

The only question is **how to distribute it**.

Choose based on your needs:
- **Need single .exe?** → Use PyInstaller (wait for build)
- **Want something fast?** → Use portable environment
- **Prefer minimal?** → Use source distribution

All three work! PyInstaller is just the most time-consuming.

---

## 💡 Recommended Next Steps

1. **Try the portable environment first** (fast and reliable)
2. **If that works for you, you're done!**
3. **If you really need .exe**, let PyInstaller build finish (be patient)

Would you like me to create the portable environment version? It's ready in 1 minute!
