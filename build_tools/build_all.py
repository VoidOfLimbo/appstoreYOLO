"""
Master build script for creating executables for all platforms.
Run this to build Windows, Linux, and Jetson versions.
"""

import sys
import subprocess
from pathlib import Path

def print_header(message):
    """Print a header message."""
    print(f"\n{'='*70}")
    print(f"  {message}")
    print(f"{'='*70}\n")

def run_builder(script_path, platform_name):
    """Run a platform-specific builder."""
    print_header(f"Building {platform_name} Version")
    
    result = subprocess.run([sys.executable, str(script_path)])
    
    if result.returncode == 0:
        print(f"\n✅ {platform_name} build completed successfully!")
        return True
    else:
        print(f"\n❌ {platform_name} build failed!")
        return False

def main():
    """Build all platform versions."""
    print_header("TensorRT Converter - Multi-Platform Builder")
    
    base_dir = Path(__file__).parent
    
    print("""
This script will build TensorRT Converter for multiple platforms:

1. 🪟 Windows (x64) - Single .exe file
2. 🐧 Linux (x86_64) - Installable package
3. 🤖 NVIDIA Jetson (ARM64) - Jetson-optimized package

Choose build targets:
  [1] Windows only
  [2] Linux only
  [3] Jetson only
  [4] All platforms
  [Q] Quit
""")
    
    choice = input("Enter choice (1-4 or Q): ").strip().upper()
    
    if choice == 'Q':
        print("Build cancelled.")
        return 0
    
    builders = {
        '1': ('build_windows_exe.py', 'Windows'),
        '2': ('build_linux.py', 'Linux'),
        '3': ('build_jetson.py', 'Jetson'),
    }
    
    results = {}
    
    if choice == '4':
        # Build all
        for script, platform in builders.values():
            results[platform] = run_builder(base_dir / script, platform)
    elif choice in builders:
        script, platform = builders[choice]
        results[platform] = run_builder(base_dir / script, platform)
    else:
        print("Invalid choice!")
        return 1
    
    # Summary
    print_header("Build Summary")
    
    for platform, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{platform:15} {status}")
    
    print("\n")
    
    if all(results.values()):
        print("🎉 All builds completed successfully!")
        print("\nOutput locations:")
        print("  - Windows: dist/windows/TensorRT_Converter_Windows.exe")
        print("  - Linux:   dist/TensorRT_Converter_Linux.tar.gz")
        print("  - Jetson:  dist/TensorRT_Converter_Jetson.tar.gz")
        return 0
    else:
        print("⚠️  Some builds failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
