# Models Directory

This directory contains machine learning models for the AppStore sub-applications.

## Structure

```
models/
├── detection/          # Object detection models
│   ├── yolo/          # YOLO models
│   ├── ssd/           # SSD models
│   └── faster_rcnn/   # Faster R-CNN models
│
├── tracking/          # Object tracking models
│   └── (tracking models)
│
├── classification/    # Image classification models
│   ├── resnet/        # ResNet models
│   ├── efficientnet/  # EfficientNet models
│   └── mobilenet/     # MobileNet models
│
└── tensorrt/          # TensorRT optimized models
    └── (optimized .trt files)
```

## Adding Models

1. Download your model files
2. Place them in the appropriate subdirectory
3. Update the app configuration to reference the model path

## Example

```python
import os

# Get model path
model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'detection')
model_path = os.path.join(model_dir, 'yolo', 'yolov8n.onnx')

# Load model
model = load_model(model_path)
```

## Supported Formats

- ONNX (.onnx)
- TensorRT (.trt, .engine)
- PyTorch (.pt, .pth)
- TensorFlow (.pb, .h5)
- Caffe (.caffemodel)

## Note

Models are not included in the repository due to size. Download them separately from:
- [YOLO Models](https://github.com/ultralytics/ultralytics)
- [TensorFlow Models](https://github.com/tensorflow/models)
- [PyTorch Hub](https://pytorch.org/hub/)
- [ONNX Model Zoo](https://github.com/onnx/models)
