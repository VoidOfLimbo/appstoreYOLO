# 📓 Training Notebooks

This directory contains Jupyter notebooks for training and fine-tuning AI models used in the AppStore application.

## 📋 Available Notebooks

### 1. `detection_training.ipynb`
**YOLOv8 Object Detection Training**

Train and fine-tune YOLOv8 models for object detection tasks.

**Features:**
- Load pre-trained YOLOv8 models (nano, small, medium, large, xlarge)
- Configure custom datasets in YOLO format
- Train with customizable hyperparameters
- Validate model performance (mAP metrics)
- Export to ONNX and TensorRT formats
- Visualize training results and metrics

**Use Cases:**
- Custom object detection
- Fine-tuning on domain-specific datasets
- Transfer learning from COCO weights

---

### 2. `classification_training.ipynb`
**YOLOv8 Image Classification Training**

Train YOLOv8 classification models for image categorization tasks.

**Features:**
- Load pre-trained YOLOv8 classification models
- Simple folder-based dataset structure
- Training with data augmentation
- Validation metrics (Top-1, Top-5 accuracy)
- Confusion matrix visualization
- Export to optimized formats

**Use Cases:**
- Image classification
- Custom category recognition
- Fine-tuning on specific image classes

---

### 3. `tracking_training.ipynb`
**YOLOv8 + StrongSORT Tracking**

Implement and optimize object tracking using YOLOv8 detection with StrongSORT.

**Features:**
- Multiple tracking algorithms (ByteTrack, BoT-SORT, StrongSORT)
- StrongSORT with Re-ID features
- Training tracking-optimized detection models
- Tracking evaluation metrics (MOTA, MOTP, IDF1)
- Real-time tracking implementation
- Export optimized tracking models

**Use Cases:**
- Multi-object tracking
- People tracking and counting
- Vehicle tracking
- Long-term tracking with Re-ID

---

## 🚀 Getting Started

### 1. Launch Jupyter Lab

From the **Training** app in AppStore:
- Click "🚀 Start Jupyter Lab"
- Jupyter Lab will open in your browser
- Navigate to the notebooks you want to use

**Or from command line:**
```bash
cd notebooks
jupyter lab
```

### 2. Download Models

Before training, download the pre-trained models:

**From the Training app:**
- Click "📦 Download Models"
- Follow the prompts to download YOLO models

**Or run the script:**
```bash
python download_models.py
```

### 3. Prepare Your Dataset

Each notebook includes detailed instructions on dataset preparation:

**Detection:** YOLO format with `data.yaml`
```
dataset/
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
└── val/
    ├── images/
    └── labels/
```

**Classification:** Folder structure
```
dataset/
├── train/
│   ├── class1/
│   ├── class2/
│   └── class3/
└── val/
    ├── class1/
    ├── class2/
    └── class3/
```

**Tracking:** Same as detection, optimized for tracking scenarios

---

## 📦 Model Download

Pre-trained models are downloaded to the `../models/` directory:

```
models/
├── detection/
│   └── yolo/          # YOLOv8 detection models
├── classification/
│   └── yolo/          # YOLOv8 classification models
├── tracking/
│   ├── yolo/          # YOLOv8 for tracking
│   └── strongsort/    # StrongSORT Re-ID models
└── tensorrt/
    ├── detection/     # TensorRT engines for detection
    ├── classification/ # TensorRT engines for classification
    └── tracking/      # TensorRT engines for tracking
```

---

## ⚙️ Training Configuration

### Common Parameters

```python
training_params = {
    'epochs': 100,           # Number of training epochs
    'imgsz': 640,           # Input image size
    'batch': 16,            # Batch size (adjust for GPU memory)
    'device': 0,            # GPU device (0, 1, 2... or 'cpu')
    'workers': 8,           # Number of data loading workers
    'optimizer': 'Adam',    # SGD, Adam, AdamW
    'lr0': 0.01,           # Initial learning rate
    'patience': 50,        # Early stopping patience
    'save': True,          # Save checkpoints
    'val': True,           # Validate during training
}
```

### GPU Acceleration

All notebooks support CUDA GPU acceleration:
- Detection: Fast training with CUDA
- Classification: GPU-accelerated data augmentation
- Tracking: Real-time tracking with TensorRT

**Check GPU availability:**
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
```

---

## 📊 Model Export

After training, export models for deployment:

### ONNX Format
```python
model.export(format='onnx', dynamic=True, simplify=True)
```

### TensorRT Format (Fastest)
```python
model.export(
    format='engine',
    device=0,
    half=True,      # FP16 precision
    workspace=4,    # Max workspace in GB
)
```

Exported TensorRT engines are automatically saved to:
- `../models/tensorrt/detection/`
- `../models/tensorrt/classification/`
- `../models/tensorrt/tracking/`

---

## 🔍 Monitoring Training

### TensorBoard Integration

YOLOv8 automatically logs to TensorBoard:
```bash
tensorboard --logdir runs/
```

### Training Metrics

All notebooks track:
- **Detection:** mAP50, mAP50-95, Precision, Recall
- **Classification:** Top-1 Accuracy, Top-5 Accuracy, Loss
- **Tracking:** MOTA, MOTP, IDF1, ID Switches

---

## 💡 Tips & Best Practices

### 1. Start Small
- Begin with smaller models (nano, small) for faster iteration
- Use small datasets to validate your pipeline
- Scale up once everything works

### 2. Data Quality
- More data ≠ better results (quality > quantity)
- Ensure balanced class distribution
- Use appropriate data augmentation

### 3. Hyperparameter Tuning
- Start with default parameters
- Adjust learning rate if training is unstable
- Increase batch size if GPU memory allows

### 4. Transfer Learning
- Always start from pre-trained weights
- Fine-tune on your domain-specific data
- Freeze early layers for faster training

### 5. Model Selection
- **Nano/Small:** Real-time applications, edge devices
- **Medium:** Balance of speed and accuracy
- **Large/XLarge:** Maximum accuracy, powerful GPUs

---

## 🐛 Troubleshooting

### CUDA Out of Memory
```python
# Reduce batch size
batch = 8  # or smaller

# Use mixed precision
fp16 = True
```

### Slow Training
```python
# Increase workers
workers = 8  # or more

# Enable caching
cache = True  # Cache images in RAM
```

### Poor Performance
- Check your dataset labels
- Increase training epochs
- Try different augmentation strategies
- Use a larger model

---

## 📚 Resources

### Official Documentation
- [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- [BoxMOT Tracking](https://github.com/mikel-brostrom/boxmot)
- [TensorRT](https://developer.nvidia.com/tensorrt)

### Datasets
- [COCO Dataset](https://cocodataset.org/)
- [Open Images](https://storage.googleapis.com/openimages/web/index.html)
- [ImageNet](https://www.image-net.org/)
- [Roboflow Universe](https://universe.roboflow.com/)

### Tutorials
- [YOLOv8 Training Guide](https://docs.ultralytics.com/modes/train/)
- [Custom Dataset Tutorial](https://docs.ultralytics.com/datasets/)
- [Model Export Guide](https://docs.ultralytics.com/modes/export/)

---

## 🤝 Integration with AppStore

After training and exporting models:

1. **Detection App:** Place `.engine` files in `models/tensorrt/detection/`
2. **Classification App:** Place `.engine` files in `models/tensorrt/classification/`
3. **Tracking App:** Place `.engine` files in `models/tensorrt/tracking/`

The apps will automatically detect and use optimized TensorRT models for inference.

---

## 📝 Creating Custom Notebooks

You can create your own training notebooks:

1. Launch Jupyter Lab from the Training app
2. Click "New" → "Notebook" → "Python 3"
3. Import required libraries:
   ```python
   from ultralytics import YOLO
   import torch
   import cv2
   import matplotlib.pyplot as plt
   ```
4. Follow the patterns in existing notebooks
5. Save in the `notebooks/` directory

---

## 🎓 Need Help?

- Check notebook comments and markdown cells
- Review the example code sections
- Consult the official Ultralytics documentation
- Open an issue in the project repository

---

**Happy Training! 🚀**
