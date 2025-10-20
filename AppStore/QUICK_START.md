# 🎯 Quick Start Guide - Training & Tracking

## 🚀 Get Started in 3 Steps

### Step 1: Download Models
```bash
python download_models.py
```
**Or** use the Training app → Click "📦 Download Models"

**Recommended:** Select option 6 (Small models) for quick testing

### Step 2: Launch Jupyter Lab
1. Open **AppStore** application
2. Click on **Training** app in sidebar
3. Click "🚀 Start Jupyter Lab"
4. Jupyter Lab opens in browser automatically

### Step 3: Train Your Model
Open any notebook:
- `detection_training.ipynb` - Object detection
- `classification_training.ipynb` - Image classification
- `tracking_training.ipynb` - Object tracking

Follow the step-by-step instructions in each notebook!

---

## 📦 Model Downloads

### Available Models

**Detection (YOLOv8):**
- `yolov8n.pt` - Nano (6.3 MB) - Fastest
- `yolov8s.pt` - Small (21.5 MB) - **Recommended**
- `yolov8m.pt` - Medium (49.7 MB)
- `yolov8l.pt` - Large (83.7 MB)
- `yolov8x.pt` - XLarge (130.5 MB) - Most accurate

**Classification (YOLOv8):**
- `yolov8n-cls.pt` - Nano (5.8 MB)
- `yolov8s-cls.pt` - Small (11.4 MB) - **Recommended**
- `yolov8m-cls.pt` - Medium (26.1 MB)

**Tracking:**
- YOLOv8 models (same as detection)
- `osnet_x0_25_msmt17.pt` - StrongSORT Re-ID (2.3 MB)

### Quick Download Commands

**Download all small models (fastest):**
```bash
python download_models.py
# Select: 6
```

**Download specific task:**
```bash
python download_models.py
# Select: 2 (Detection only)
# Select: 3 (Classification only)
# Select: 4 (Tracking only)
```

---

## 🎓 Training Workflows

### Train Object Detection

1. **Prepare Dataset** (YOLO format):
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

2. **Open Notebook:**
   - Launch Jupyter Lab from Training app
   - Open `detection_training.ipynb`

3. **Train:**
   ```python
   from ultralytics import YOLO
   model = YOLO('yolov8s.pt')
   results = model.train(
       data='path/to/data.yaml',
       epochs=100,
       imgsz=640,
       batch=16
   )
   ```

4. **Export to TensorRT:**
   ```python
   model.export(format='engine', device=0, half=True)
   ```

### Train Classification

1. **Prepare Dataset** (folder structure):
   ```
   dataset/
   ├── train/
   │   ├── cat/
   │   ├── dog/
   │   └── bird/
   └── val/
       ├── cat/
       ├── dog/
       └── bird/
   ```

2. **Open Notebook:**
   - Open `classification_training.ipynb`

3. **Train:**
   ```python
   model = YOLO('yolov8s-cls.pt')
   results = model.train(
       data='path/to/dataset',
       epochs=100,
       imgsz=224,
       batch=32
   )
   ```

### Setup Object Tracking

1. **Download StrongSORT Model:**
   ```bash
   python download_models.py
   # Select: 5 (StrongSORT)
   ```

2. **Open Tracking App:**
   - Select **StrongSORT** from dropdown
   - View tracker configuration

3. **Use in Code:**
   ```python
   from boxmot import StrongSORT
   tracker = StrongSORT(
       model_weights='models/tracking/strongsort/osnet_x0_25_msmt17.pt',
       device='cuda:0',
       fp16=True
   )
   ```

---

## 🎯 Using Trained Models

### In Detection App
1. Export model to `models/tensorrt/detection/model.engine`
2. Open **Detection** app
3. App automatically uses TensorRT model for fast inference

### In Classification App
1. Export model to `models/tensorrt/classification/model.engine`
2. Open **Classification** app
3. Enjoy accelerated classification

### In Tracking App
1. Export model to `models/tensorrt/tracking/model.engine`
2. Select **StrongSORT** or other tracker
3. Use for multi-object tracking

---

## ⚙️ Configuration Tips

### GPU Memory Optimization
```python
# If you get CUDA out of memory:
batch = 8        # Reduce batch size
workers = 4      # Reduce workers
cache = False    # Disable caching
```

### Training Speed
```python
# For faster training:
batch = 32       # Increase batch size (if GPU allows)
workers = 8      # More workers
cache = True     # Cache images in RAM
imgsz = 320      # Smaller image size
```

### Best Accuracy
```python
# For best results:
epochs = 300     # More epochs
imgsz = 1280     # Larger images
model = 'yolov8x'  # Larger model
augment = True   # Enable augmentation
```

---

## 🐛 Troubleshooting

### Jupyter Lab Won't Start
```bash
# Install/reinstall Jupyter
pip install --upgrade jupyterlab

# Or from Training app:
# Click "🚀 Start Jupyter Lab" - logs show errors
```

### Models Not Found
```bash
# Download models first:
python download_models.py

# Check models directory:
# AppStore/models/ should have subdirectories
```

### StrongSORT Not Available
```bash
# Install boxmot:
pip install boxmot

# Verify installation:
python -c "from boxmot import StrongSORT; print('OK')"
```

### Training Too Slow
- Reduce `batch` size
- Reduce `imgsz` (image size)
- Use smaller model (n or s)
- Enable `cache=True`
- Check GPU usage: `nvidia-smi`

---

## 📚 Quick Reference

### Common Training Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| `epochs` | 100 | Training epochs |
| `imgsz` | 640 | Image size |
| `batch` | 16 | Batch size |
| `device` | 0 | GPU device (0, 1, ...) |
| `lr0` | 0.01 | Initial learning rate |
| `patience` | 50 | Early stopping |

### Model Sizes Comparison
| Model | Size | Speed | mAP | Best For |
|-------|------|-------|-----|----------|
| n | 6MB | Fastest | 37.3 | Edge devices |
| s | 22MB | Fast | 44.9 | **General use** |
| m | 50MB | Medium | 50.2 | Balanced |
| l | 84MB | Slow | 52.9 | Accuracy |
| x | 131MB | Slowest | 54.0 | Max accuracy |

### Export Formats
| Format | Speed | Use Case |
|--------|-------|----------|
| `.pt` | Medium | Training/Python |
| `.onnx` | Fast | Cross-platform |
| `.engine` | Fastest | **Production (NVIDIA)** |

---

## 🎊 Features Summary

### What You Can Do Now:
- ✅ Download pre-trained YOLO models
- ✅ Train custom detection models
- ✅ Train custom classification models
- ✅ Setup advanced object tracking
- ✅ Export to TensorRT for fast inference
- ✅ Run Jupyter notebooks from the app
- ✅ Use StrongSORT with Re-ID
- ✅ Monitor training in real-time
- ✅ Manage models and notebooks easily

### 5 Apps Available:
1. **Detection** - Object detection with YOLO
2. **Classification** - Image classification
3. **Tracking** - Multi-object tracking with StrongSORT
4. **TensorRT Converter** - Model optimization
5. **Training** - Jupyter Lab integration

---

## 🔗 Useful Links

- **Ultralytics Docs:** https://docs.ultralytics.com/
- **BoxMOT GitHub:** https://github.com/mikel-brostrom/boxmot
- **TensorRT Guide:** https://developer.nvidia.com/tensorrt
- **YOLO Tutorial:** https://docs.ultralytics.com/quickstart/

---

## 💡 Pro Tips

1. **Start Small:** Use small models and datasets first
2. **Use TensorRT:** Always export to `.engine` for production
3. **Monitor GPU:** Use `nvidia-smi` to check utilization
4. **Save Checkpoints:** Training auto-saves every 10 epochs
5. **Validate Often:** Set `val=True` to track progress
6. **Use Transfer Learning:** Always start from pre-trained weights

---

**Need help?** Check the detailed notebooks README: `notebooks/README.md`

**Happy Training! 🚀**
