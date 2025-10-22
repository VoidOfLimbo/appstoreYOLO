"""
Test script for TensorRT Model Converter
Run this to verify all components are working.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.hardware_detector import HardwareDetector
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def test_hardware_detection():
    """Test hardware detection functionality."""
    print("=" * 60)
    print("Testing Hardware Detection")
    print("=" * 60)
    
    try:
        detector = HardwareDetector()
        hw_info = detector.detect()
        
        print("\n" + detector.get_summary(hw_info))
        print("\n✅ Hardware detection test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Hardware detection test failed: {e}")
        logger.error(f"Hardware detection test failed: {e}", exc_info=True)
        return False


def test_imports():
    """Test that all required packages can be imported."""
    print("\n" + "=" * 60)
    print("Testing Package Imports")
    print("=" * 60)
    
    packages = {
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'tensorrt': 'TensorRT',
        'onnx': 'ONNX',
        'PyQt5': 'PyQt5',
        'PyQt5.QtWidgets': 'PyQt5 Widgets',
        'numpy': 'NumPy',
        'PIL': 'Pillow',
    }
    
    all_passed = True
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name:20s} - OK")
        except ImportError as e:
            print(f"❌ {name:20s} - FAILED: {e}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All package import tests passed!")
    else:
        print("\n❌ Some package imports failed!")
    
    return all_passed


def test_directory_structure():
    """Test that all required directories exist."""
    print("\n" + "=" * 60)
    print("Testing Directory Structure")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    required_dirs = [
        'src',
        'src/gui',
        'src/utils',
        'logs',
        'output',
    ]
    
    required_files = [
        'main.py',
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'tensorrt_converter.spec',
        'src/config.py',
        'src/gui/main_window.py',
        'src/utils/hardware_detector.py',
        'src/utils/tensorrt_converter.py',
        'src/utils/logger.py',
    ]
    
    all_passed = True
    
    print("\nChecking directories:")
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"✅ {dir_path:30s} - OK")
        else:
            print(f"❌ {dir_path:30s} - MISSING")
            all_passed = False
    
    print("\nChecking files:")
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path:50s} - OK")
        else:
            print(f"❌ {file_path:50s} - MISSING")
            all_passed = False
    
    if all_passed:
        print("\n✅ Directory structure test passed!")
    else:
        print("\n❌ Some directories or files are missing!")
    
    return all_passed


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  TensorRT Model Converter - System Tests  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    tests = [
        ("Package Imports", test_imports),
        ("Directory Structure", test_directory_structure),
        ("Hardware Detection", test_hardware_detection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            logger.error(f"{test_name} crashed: {e}", exc_info=True)
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status:10s} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\nTo run the GUI application:")
        print("  python main.py")
        print("\nTo build the executable:")
        print("  pyinstaller tensorrt_converter.spec")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
