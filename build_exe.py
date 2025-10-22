"""
Build script for creating the standalone executable.
This script builds the TensorRT Model Converter as a portable .exe
"""
import sys
import subprocess
from pathlib import Path
import shutil

def main():
    print("=" * 60)
    print("TensorRT Model Converter - Build Script")
    print("=" * 60)
    print()
    
    base_dir = Path(__file__).parent
    spec_file = base_dir / "tensorrt_converter.spec"
    
    if not spec_file.exists():
        print("❌ Error: tensorrt_converter.spec not found!")
        return 1
    
    print("📦 Building executable with PyInstaller...")
    print(f"   Spec file: {spec_file}")
    print()
    
    try:
        # Run PyInstaller
        result = subprocess.run(
            ["pyinstaller", str(spec_file), "--clean"],
            cwd=str(base_dir),
            check=True
        )
        
        if result.returncode == 0:
            dist_dir = base_dir / "dist" / "TensorRT_Converter"
            
            if dist_dir.exists():
                print()
                print("=" * 60)
                print("✅ Build completed successfully!")
                print("=" * 60)
                print()
                print(f"Executable location: {dist_dir}")
                print(f"Main executable: {dist_dir / 'TensorRT_Converter.exe'}")
                print()
                print("To distribute:")
                print(f"  1. Copy the entire '{dist_dir.name}' folder")
                print("  2. Run TensorRT_Converter.exe on the target machine")
                print()
                print("Note: The target machine needs:")
                print("  - NVIDIA GPU with CUDA support")
                print("  - Latest NVIDIA drivers")
                print("  - TensorRT runtime (if not embedded)")
                print()
                
                # Calculate size
                total_size = sum(f.stat().st_size for f in dist_dir.rglob('*') if f.is_file())
                size_mb = total_size / (1024 * 1024)
                print(f"Total package size: {size_mb:.2f} MB")
                print()
                
            else:
                print("⚠️  Build completed but dist directory not found!")
                return 1
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print()
        print("❌ Build failed!")
        print(f"Error: {e}")
        return 1
    
    except Exception as e:
        print()
        print("❌ Unexpected error during build!")
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
