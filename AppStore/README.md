# AppStore - Modular Application Framework

A modular Python application framework with a PyQt5 dashboard that supports dynamic loading of pluggable sub-applications. Features include hardware acceleration support, version-aware installation, and easy deployment.

## 🚀 Features

- **Modular Architecture**: Plug-and-play sub-applications
- **Dynamic Loading**: Apps are loaded at runtime from the `apps/` directory
- **PyQt5 UI**: Modern, responsive dashboard interface
- **Hardware Acceleration**: Support for OpenCV and TensorRT
- **Version Management**: Automatic version checking and updates
- **Easy Deployment**: One-click build to `.exe` and installer creation
- **Update System**: Smart installer that compares versions before updating

## 📁 Project Structure

```
AppStore/
├── main.py                      # Entry point with main UI dashboard
├── setup.py                     # PyInstaller build script
├── AppStore.spec               # PyInstaller specification
├── requirements.txt            # Python dependencies
│
├── main_app/                   # Main application package
│   ├── __init__.py
│   ├── ui/                     # UI components
│   │   └── __init__.py
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       ├── base_app.py        # Base class for sub-apps
│       └── app_loader.py      # Dynamic app loader
│
├── apps/                       # Pluggable sub-applications
│   ├── detection/             # Object detection app
│   │   ├── config.json
│   │   └── detection.py
│   ├── tracking/              # Object tracking app
│   │   ├── config.json
│   │   └── tracking.py
│   ├── classification/        # Image classification app
│   │   ├── config.json
│   │   └── classification.py
│   └── tensorrt_converter/    # TensorRT model converter
│       ├── config.json
│       └── tensorrt_converter.py
│
├── config/                     # Configuration files
│   ├── version.txt            # Current version
│   └── version_manager.py     # Version comparison logic
│
├── assets/                     # Images, icons, models
│   └── (place icon.ico here)
│
└── installer/                  # Installer scripts
    ├── AppStore.iss           # Inno Setup script
    └── output/                # Generated installers
```

## 🛠️ Setup Instructions

### 1. Clone or Download the Project

```bash
cd c:\Users\John\Documents\python\AppStore
```

### 2. Create Virtual Environment (Already Done ✓)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies (Already Done ✓)

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## 📦 Building the Executable

### Method 1: Using setup.py (Recommended)

```bash
python setup.py
```

This will create the executable in `dist/AppStore/`

### Method 2: Using PyInstaller Directly

```bash
pyinstaller AppStore.spec
```

### Method 3: Manual PyInstaller Command

```bash
pyinstaller --name=AppStore --onedir --windowed ^
    --add-data="apps;apps" ^
    --add-data="config;config" ^
    --add-data="assets;assets" ^
    --hidden-import=cv2 ^
    main.py
```

## 📀 Creating the Installer

### Prerequisites

1. Build the application executable (see above)
2. Download and install [Inno Setup](https://jrsoftware.org/isdl.php)

### Steps

1. Open Inno Setup Compiler
2. Open the file: `installer\AppStore.iss`
3. Click "Build" → "Compile"
4. The installer will be created in `installer\output\`

### Installer Features

- ✅ Checks if app is already installed
- ✅ Compares installed version with new version
- ✅ Updates only if new version is newer
- ✅ Warns user if attempting to downgrade
- ✅ Preserves user settings during updates
- ✅ Creates desktop shortcut (optional)
- ✅ Adds to Start Menu

## 🔧 Creating a New Sub-Application

### 1. Create App Directory

```bash
mkdir apps\my_new_app
```

### 2. Create config.json

```json
{
  "name": "My New App",
  "version": "1.0.0",
  "description": "Description of my app",
  "enabled": true,
  "author": "Your Name",
  "dependencies": ["numpy"]
}
```

### 3. Create App Module (my_new_app.py)

```python
import sys
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from main_app.utils.base_app import BaseApp


class MyNewApp(BaseApp):
    """My new application."""
    
    def initialize(self) -> bool:
        """Initialize the app."""
        print(f"Initializing {self.name}...")
        # Your initialization code here
        return True
    
    def create_widget(self) -> QWidget:
        """Create the UI widget."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        title = QLabel(f"<h2>{self.name}</h2>")
        layout.addWidget(title)
        
        # Add your UI components here
        
        return widget
    
    def process(self, data):
        """Process input data."""
        # Your processing logic here
        return data
    
    def cleanup(self):
        """Clean up resources."""
        print(f"Cleaning up {self.name}...")
```

### 4. Restart the Application

The new app will be automatically discovered and loaded!

## 🔄 Updating the Version

1. Edit `config\version.txt` with the new version number (e.g., `1.1.0`)
2. Update the version in `installer\AppStore.iss`:
   ```pascal
   #define MyAppVersion "1.1.0"
   ```
3. Rebuild the executable and installer

## 📝 Configuration Files

### config.json (for each sub-app)

- `name`: Display name of the app
- `version`: App version
- `description`: Brief description
- `enabled`: Whether the app is enabled
- `author`: Developer name
- `dependencies`: Required Python packages

### version.txt

Contains the current application version (e.g., `1.0.0`)

## � Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[Installation Guide](docs/INSTALL.md)** - Detailed setup instructions
- **[CUDA Setup Guide](docs/CUDA_SETUP.md)** - GPU acceleration configuration
- **[YOLO Versions](docs/YOLO_VERSIONS.md)** - Model version and size selection
- **[Git Guide](docs/GIT_GUIDE.md)** - Version control best practices

## 🖥️ Hardware Acceleration - CUDA 13.0 ✓

The application is configured with **CUDA 13.0** support for GPU acceleration!

**Installed GPU Packages:**
- ✅ **TensorRT 10.13.3.9** - Model inference optimization
- ✅ **CuPy 13.6.0** - GPU array operations (CUDA 13.x)
- ✅ **OpenCV 4.12.0** - Computer vision with contrib modules
- ✅ **CUDA Runtime** - NVIDIA CUDA 13.0 libraries

**Performance:** 10-50x faster for large operations!

See **[CUDA Setup Guide](docs/CUDA_SETUP.md)** for complete details.

## 🐛 Debugging

### Run with Console Window

Edit `AppStore.spec` and change:
```python
console=True,  # Show console for debugging
```

Then rebuild with PyInstaller.

### Check Logs

When running from source, logs appear in the console.

## 📚 Dependencies

- **Python**: 3.8+
- **PyQt5**: GUI framework
- **OpenCV**: Computer vision operations
- **NumPy**: Numerical operations
- **Pillow**: Image processing
- **Matplotlib**: Plotting and visualization
- **PyInstaller**: Executable creation
- **TensorRT**: (Optional) Hardware acceleration

## 🤝 Contributing

To add new features or sub-applications:

1. Follow the modular architecture
2. Inherit from `BaseApp` for new apps
3. Add proper configuration files
4. Update documentation

## 📄 License

Copyright (C) 2025 AppStore Team

## 🔗 Links

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)

## 💡 Tips

1. **Testing**: Always test the executable before creating the installer
2. **Icons**: Place a 256x256 `icon.ico` file in the `assets/` folder
3. **Models**: Store ML models in `assets/` and reference them in your app
4. **Updates**: Users can simply run the new installer to update automatically
5. **Plugins**: Drop new apps into the `apps/` folder without rebuilding

## 🎯 Next Steps

1. Run the application: `python main.py`
2. Test all sub-applications
3. Customize the UI and add your own apps
4. Build the executable: `python setup.py`
5. Create the installer using Inno Setup
6. Deploy to users!

---

**Enjoy building modular applications with AppStore!** 🎉
