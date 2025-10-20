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
    
    # YOLO model URLs (Ultralytics)
    YOLO_MODELS = {
        'detection': {
            'yolov8n': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt',
            'yolov8s': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt',
            'yolov8m': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt',
            'yolov8l': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8l.pt',
            'yolov8x': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt',
        },
        'classification': {
            'yolov8n-cls': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-cls.pt',
            'yolov8s-cls': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s-cls.pt',
            'yolov8m-cls': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m-cls.pt',
        },
        'tracking': {
            'yolov8n': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt',
            'yolov8s': 'https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt',
        }
    }
    
    def __init__(self, base_dir=None):
        """Initialize the model downloader.
        
        Args:
            base_dir: Base directory for models (defaults to ./models)
        """
        if base_dir is None:
            base_dir = Path(__file__).parent / 'models'
        self.base_dir = Path(base_dir)
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
    
    def download_yolo_models(self, task='all', size='small'):
        """Download YOLO models for specific tasks.
        
        Args:
            task: 'detection', 'classification', 'tracking', or 'all'
            size: 'nano', 'small', 'medium', 'large', 'xlarge', or 'all'
        """
        size_map = {
            'nano': 'n',
            'small': 's',
            'medium': 'm',
            'large': 'l',
            'xlarge': 'x'
        }
        
        tasks = ['detection', 'classification', 'tracking'] if task == 'all' else [task]
        
        for task_name in tasks:
            if task_name not in self.YOLO_MODELS:
                continue
                
            print(f"\n📦 Downloading {task_name} models...")
            
            for model_name, url in self.YOLO_MODELS[task_name].items():
                # Filter by size if specified
                if size != 'all':
                    size_code = size_map.get(size, 's')
                    if size_code not in model_name:
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
    
    downloader = ModelDownloader()
    
    print("\nAvailable options:")
    print("1. Download all YOLO models (detection, classification, tracking)")
    print("2. Download detection models only")
    print("3. Download classification models only")
    print("4. Download tracking models only")
    print("5. Download StrongSORT model")
    print("6. Download small models only (recommended for testing)")
    print("7. List downloaded models")
    print("0. Exit")
    
    while True:
        choice = input("\nSelect an option (0-7): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            downloader.download_yolo_models(task='all', size='all')
            downloader.download_strongsort_model()
        elif choice == '2':
            downloader.download_yolo_models(task='detection', size='all')
        elif choice == '3':
            downloader.download_yolo_models(task='classification', size='all')
        elif choice == '4':
            downloader.download_yolo_models(task='tracking', size='all')
            downloader.download_strongsort_model()
        elif choice == '5':
            downloader.download_strongsort_model()
        elif choice == '6':
            print("\nDownloading small models (nano and small sizes)...")
            downloader.download_yolo_models(task='all', size='small')
            downloader.download_strongsort_model()
        elif choice == '7':
            downloader.list_models()
        else:
            print("❌ Invalid option. Please try again.")
    
    print("\n✅ Model download complete!")
    downloader.list_models()


if __name__ == '__main__':
    main()
