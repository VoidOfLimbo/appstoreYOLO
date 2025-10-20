"""Setup script for building the application with PyInstaller.

Usage:
    python setup.py
    
This will create an executable in the dist/ folder.
"""

import os
import sys
import PyInstaller.__main__

# Get the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths
MAIN_SCRIPT = os.path.join(BASE_DIR, 'main.py')
ICON_PATH = os.path.join(BASE_DIR, 'assets', 'icon.ico')  # Optional

# PyInstaller arguments
pyinstaller_args = [
    MAIN_SCRIPT,
    '--name=AppStore',
    '--onedir',  # Create a directory with all dependencies
    '--windowed',  # No console window (GUI app)
    '--clean',  # Clean PyInstaller cache
    
    # Add data files
    f'--add-data={os.path.join(BASE_DIR, "apps")}{os.pathsep}apps',
    f'--add-data={os.path.join(BASE_DIR, "config")}{os.pathsep}config',
    f'--add-data={os.path.join(BASE_DIR, "assets")}{os.pathsep}assets',
    
    # Hidden imports (modules that PyInstaller might miss)
    '--hidden-import=cv2',
    '--hidden-import=numpy',
    '--hidden-import=PIL',
    '--hidden-import=PyQt5',
    '--hidden-import=matplotlib',
    
    # Exclude unnecessary modules to reduce size
    '--exclude-module=tkinter',
    '--exclude-module=unittest',
    '--exclude-module=test',
    
    # Output directory
    '--distpath=dist',
    '--workpath=build',
    '--specpath=.',
]

# Add icon if it exists
if os.path.exists(ICON_PATH):
    pyinstaller_args.append(f'--icon={ICON_PATH}')

def main():
    """Run PyInstaller with the specified arguments."""
    print("=" * 60)
    print("Building AppStore executable with PyInstaller")
    print("=" * 60)
    print(f"Main script: {MAIN_SCRIPT}")
    print(f"Output directory: {os.path.join(BASE_DIR, 'dist')}")
    print()
    
    try:
        PyInstaller.__main__.run(pyinstaller_args)
        print()
        print("=" * 60)
        print("Build completed successfully!")
        print(f"Executable location: {os.path.join(BASE_DIR, 'dist', 'AppStore')}")
        print("=" * 60)
    except Exception as e:
        print(f"Error during build: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
