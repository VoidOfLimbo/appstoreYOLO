
import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path

def build_installer():
    """Build the GUI installer executable."""
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("=" * 60)
    print("  Building TensorRT Converter GUI Installer")
    print("=" * 60)
    
    # Create app_files.zip with all application files
    print("\nCreating application archive...")
    import zipfile
    
    zip_path = project_root / "build_tools" / "app_files.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add main files
        for file in ['main.py', 'requirements.txt', 'README.md']:
            file_path = project_root / file
            if file_path.exists():
                zipf.write(file_path, file)
                print(f"  Added: {file}")
        
        # Add directories
        for dir_name in ['src', 'config', 'assets']:
            dir_path = project_root / dir_name
            if dir_path.exists():
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        file_path = Path(root) / file
                        arc_path = file_path.relative_to(project_root)
                        zipf.write(file_path, arc_path)
                        print(f"  Added: {arc_path}")
    
    print(f"\n✓ Application archive created: {zip_path}")
    
    # Clean previous builds
    print("\nCleaning previous builds...")
    for path in [project_root / "build", project_root / "dist" / "setup"]:
        if path.exists():
            shutil.rmtree(path)
            print(f"  Removed: {path}")
    
    # PyInstaller arguments
    print("\\nBuilding installer executable...")
    args = [
        'build_tools/installer_gui.py',
        '--name=TensorRT_Converter_Setup',
        '--onefile',
        '--windowed',
        # Skip icon for now - can be added later with a tool
        '--add-data=build_tools/app_files.zip;.',
        '--hidden-import=PyQt5',
        '--hidden-import=winshell',
        '--hidden-import=win32com.client',
        '--collect-all=PyQt5',
        f'--distpath={project_root / "dist" / "setup"}',
        f'--workpath={project_root / "build"}',
        '--clean',
        '--noconfirm',
    ]
    
    try:
        PyInstaller.__main__.run(args)
        
        print("\n" + "=" * 60)
        print("  ✓ Installer built successfully!")
        print("=" * 60)
        
        exe_path = project_root / "dist" / "setup" / "TensorRT_Converter_Setup.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n📦 Installer Location:")
            print(f"   {exe_path}")
            print(f"   Size: {size_mb:.1f} MB")
            print(f"\n🚀 Distribution:")
            print(f"   Share this single .exe file with users")
            print(f"   Users run it to install TensorRT Converter")
            print(f"\n✨ Features:")
            print(f"   • GUI wizard installation")
            print(f"   • System requirements check")
            print(f"   • Custom installation path")
            print(f"   • Automatic dependency installation")
            print(f"   • Desktop shortcut creation")
        else:
            print(f"\n❌ Installer not found at: {exe_path}")
        
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    build_installer()
