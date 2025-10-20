# Installation Instructions for AppStore

## For End Users

### Installing from Installer
1. Download the installer: `AppStore_Setup_1.0.0.exe`
2. Run the installer
3. Follow the installation wizard
4. The installer will:
   - Check if an older version is installed
   - Compare versions automatically
   - Update only if the new version is newer
   - Create desktop and start menu shortcuts

### Updating
1. Download the new installer
2. Run it - the installer will:
   - Detect your current version
   - Show version comparison
   - Ask for confirmation to upgrade
   - Preserve your settings

### Uninstalling
1. Go to Control Panel → Programs and Features
2. Find "AppStore" and click Uninstall
3. Or use the uninstaller from the Start Menu

## For Developers

### Development Setup
1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python main.py`

### Quick Testing
```powershell
.\run.ps1
```

### Building Executable
```powershell
.\build.ps1
```

Or manually:
```powershell
python setup.py
```

### Creating Installer
1. Build the executable first
2. Install Inno Setup from https://jrsoftware.org/isdl.php
3. Open `installer\AppStore.iss` in Inno Setup Compiler
4. Click Build → Compile
5. Find the installer in `installer\output\`

### Version Management
1. Update version in `config\version.txt`
2. Update version in `installer\AppStore.iss` (#define MyAppVersion)
3. Update version in `main_app\__init__.py`
4. Rebuild and create new installer

### Adding New Sub-Apps
1. Create folder in `apps\` (e.g., `apps\my_app\`)
2. Create `config.json` with app metadata
3. Create Python module inheriting from `BaseApp`
4. Implement required methods: `initialize()`, `create_widget()`, `process()`
5. Restart the application - it will auto-load!

### Testing the Installer
1. Build the executable
2. Create the installer
3. Install on a test machine or VM
4. Verify all features work
5. Update the version and test the update process

## System Requirements

### Runtime Requirements
- Windows 10 or later (64-bit)
- 4 GB RAM minimum (8 GB recommended)
- 500 MB disk space
- For TensorRT apps: NVIDIA GPU with CUDA support

### Development Requirements
- Python 3.8 or later
- Windows 10 or later
- Visual Studio Build Tools (for some packages)
- Git (optional)
- Inno Setup (for creating installers)

## Troubleshooting

### Application won't start
- Check if all dependencies are installed
- Try running from command line to see errors
- Check Windows Event Viewer for crash logs

### Sub-apps not loading
- Verify `apps\` folder structure
- Check `config.json` syntax
- Look for errors in console output

### Build fails
- Ensure virtual environment is activated
- Update PyInstaller: `pip install --upgrade pyinstaller`
- Check for missing dependencies

### Installer issues
- Ensure executable is built first
- Check version number format (X.Y.Z)
- Run Inno Setup as administrator

## Support

For issues, check:
1. README.md for documentation
2. Console output for errors
3. Log files in the app directory

---

Happy coding! 🚀
