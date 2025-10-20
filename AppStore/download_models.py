"""
Model Download and Management Script

This script downloads YOLO models for detection, classification, and tracking,
and prepares the model directory structure.
"""

import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm
import hashlib


class ModelDownloader:
    """Downloads and manages AI models for the AppStore."""
    
    # YOLO model URLs by version (Ultralytics)
    YOLO_VERSIONS = {
        'v8': {
            'detection': {
                'yolov8n': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt',
                'yolov8s': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt',
                'yolov8m': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8m.pt',
                'yolov8l': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8l.pt',
                'yolov8x': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8x.pt',
            },
            'classification': {
                'yolov8n-cls': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-cls.pt',
                'yolov8s-cls': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s-cls.pt',
                'yolov8m-cls': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8m-cls.pt',
            },
            'tracking': {
                'yolov8n': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt',
                'yolov8s': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt',
            }
        },
        'v11': {
            'detection': {
                'yolo11n': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt',
                'yolo11s': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt',
                'yolo11m': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11m.pt',
                'yolo11l': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11l.pt',
                'yolo11x': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11x.pt',
            },
            'classification': {
                'yolo11n-cls': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n-cls.pt',
                'yolo11s-cls': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s-cls.pt',
                'yolo11m-cls': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11m-cls.pt',
            },
            'tracking': {
                'yolo11n': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt',
                'yolo11s': 'https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11s.pt',
            }
        }
    }
    
    def __init__(self, base_dir=None, yolo_version='v11'):
        """Initialize the model downloader.
        
        Args:
            base_dir: Base directory for models (defaults to ./models)
            yolo_version: YOLO version to download ('v8' or 'v11', default: 'v11')
        """
        if base_dir is None:
            base_dir = Path(__file__).parent / 'models'
        self.base_dir = Path(base_dir)
        self.yolo_version = yolo_version
        self.yolo_models = self.YOLO_VERSIONS.get(yolo_version, self.YOLO_VERSIONS['v11'])
        self.setup_directories()
    
    def setup_directories(self):
        """Create the directory structure for models."""
        directories = [
            'detection/yolo',
            'classification/yolo',
            'tracking/yolo',
            'tracking/strongsort',
            'tensorrt/detection',
            'tensorrt/classification',
            'tensorrt/tracking',
        ]
        
        for dir_path in directories:
            full_path = self.base_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {full_path}")
    
    def download_file(self, url, dest_path, desc=None):
        """Download a file with progress bar.
        
        Args:
            url: URL to download from
            dest_path: Destination file path
            desc: Description for progress bar
            
        Returns:
            bool: True if successful
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(dest_path, 'wb') as file, tqdm(
                desc=desc or dest_path.name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    progress_bar.update(size)
            
            print(f"✓ Downloaded: {dest_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error downloading {url}: {e}")
            return False
    
    def download_yolo_models(self, task='all', size='s'):
        """Download YOLO models for specific tasks.
        
        Args:
            task: 'detection', 'classification', 'tracking', or 'all'
            size: Size code 'n', 's', 'm', 'l', 'x', or 'all'
        """
        tasks = ['detection', 'classification', 'tracking'] if task == 'all' else [task]
        
        print(f"\n🎯 Using YOLO {self.yolo_version.upper()} models")
        
        for task_name in tasks:
            if task_name not in self.yolo_models:
                continue
                
            print(f"\n📦 Downloading {task_name} models...")
            
            for model_name, url in self.yolo_models[task_name].items():
                # Filter by size if specified (size is now a code: 'n', 's', 'm', 'l', 'x')
                if size != 'all':
                    # Check if the size code is in the model name
                    # For yolo11n, yolo11s, yolo11m, etc.
                    if not model_name.endswith(size) and not model_name.endswith(f'{size}-cls'):
                        continue
                
                dest_dir = self.base_dir / task_name / 'yolo'
                dest_path = dest_dir / f"{model_name}.pt"
                
                if dest_path.exists():
                    print(f"⏭️  Skipping {model_name} (already exists)")
                    continue
                
                self.download_file(url, dest_path, f"Downloading {model_name}")
    
    def download_strongsort_model(self):
        """Download StrongSORT tracking model."""
        print(f"\n📦 Downloading StrongSORT model...")
        
        # StrongSORT OSNet model
        url = "https://github.com/mikel-brostrom/yolov8_tracking/releases/download/v9.0/osnet_x0_25_msmt17.pt"
        dest_dir = self.base_dir / 'tracking' / 'strongsort'
        dest_path = dest_dir / 'osnet_x0_25_msmt17.pt'
        
        if dest_path.exists():
            print(f"⏭️  StrongSORT model already exists")
            return
        
        self.download_file(url, dest_path, "Downloading StrongSORT OSNet")
    
    def list_models(self):
        """List all downloaded models."""
        print("\n📋 Downloaded Models:")
        print("=" * 70)
        
        for task in ['detection', 'classification', 'tracking']:
            task_dir = self.base_dir / task
            if task_dir.exists():
                models = list(task_dir.rglob('*.pt')) + list(task_dir.rglob('*.onnx'))
                if models:
                    print(f"\n{task.upper()}:")
                    for model in models:
                        size_mb = model.stat().st_size / (1024 * 1024)
                        rel_path = model.relative_to(self.base_dir)
                        print(f"  ✓ {rel_path} ({size_mb:.1f} MB)")
        
        # TensorRT models
        tensorrt_dir = self.base_dir / 'tensorrt'
        if tensorrt_dir.exists():
            engines = list(tensorrt_dir.rglob('*.engine')) + list(tensorrt_dir.rglob('*.trt'))
            if engines:
                print(f"\nTENSORRT ENGINES:")
                for engine in engines:
                    size_mb = engine.stat().st_size / (1024 * 1024)
                    rel_path = engine.relative_to(self.base_dir)
                    print(f"  ⚡ {rel_path} ({size_mb:.1f} MB)")


def main():
    """Main function."""
    print("=" * 70)
    print("🚀 AppStore Model Downloader")
    print("=" * 70)
    
    # Version selection
    print("\n📌 Select YOLO Version:")
    print("1. YOLO v11 (Latest, Best Performance) - RECOMMENDED ⭐")
    print("2. YOLO v8 (Stable, Well-tested)")
    
    version_choice = input("\nSelect version (1-2, default=1): ").strip() or '1'
    
    if version_choice == '2':
        yolo_version = 'v8'
        print("✓ Selected YOLO v8")
    else:
        yolo_version = 'v11'
        print("✓ Selected YOLO v11 (Default)")
    
    # Model size selection
    print("\n📏 Select Default Model Size:")
    print("1. Nano (n) - Smallest, Fastest (~3MB)")
    print("2. Small (s) - Balanced, Good for testing (~11MB)")
    print("3. Medium (m) - RECOMMENDED ⭐ (~25MB)")
    print("4. Large (l) - High accuracy (~43MB)")
    print("5. XLarge (x) - Best accuracy (~68MB)")
    print("6. All sizes - Download everything")
    
    size_choice = input("\nSelect size (1-6, default=3): ").strip() or '3'
    
    size_map = {
        '1': ('nano', 'n'),
        '2': ('small', 's'),
        '3': ('medium', 'm'),
        '4': ('large', 'l'),
        '5': ('xlarge', 'x'),
        '6': ('all', 'all')
    }
    
    size_name, size_code = size_map.get(size_choice, ('medium', 'm'))
    print(f"✓ Selected {size_name.upper()} models (Default: Medium)")
    
    downloader = ModelDownloader(yolo_version=yolo_version)
    
    print("\n" + "=" * 70)
    print(f"📦 Downloading YOLO {yolo_version.upper()} - {size_name.upper()} Models")
    print("=" * 70)
    
    print("\nAvailable options:")
    print(f"1. Download all YOLO models for {size_name.upper()} size (detection, classification, tracking)")
    print(f"2. Download detection models only ({size_name.upper()})")
    print(f"3. Download classification models only ({size_name.upper()})")
    print(f"4. Download tracking models only ({size_name.upper()})")
    print("5. Download StrongSORT model")
    print("6. List downloaded models")
    print("7. Change settings (version/size)")
    print("0. Exit")
    
    while True:
        choice = input("\nSelect an option (0-7): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            downloader.download_yolo_models(task='all', size=size_code)
            downloader.download_strongsort_model()
        elif choice == '2':
            downloader.download_yolo_models(task='detection', size=size_code)
        elif choice == '3':
            downloader.download_yolo_models(task='classification', size=size_code)
        elif choice == '4':
            downloader.download_yolo_models(task='tracking', size=size_code)
            downloader.download_strongsort_model()
        elif choice == '5':
            downloader.download_strongsort_model()
        elif choice == '6':
            downloader.list_models()
        elif choice == '7':
            # Change settings and restart
            print("\n" + "=" * 70)
            main()
            return
        else:
            print("❌ Invalid option. Please try again.")
    
    print("\n✅ Model download complete!")
    downloader.list_models()


if __name__ == '__main__':
    main()
