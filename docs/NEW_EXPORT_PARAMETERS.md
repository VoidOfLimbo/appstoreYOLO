# New Export Parameters Added

## Overview

Enhanced the TensorRT Converter GUI with additional export parameters for fine-tuned model optimization and multi-format support.

## New Parameters

### 1. **Image Size** (imgsz)
- **UI Element**: Dropdown menu
- **Options**: 320, 416, 512, 640, 800, 1024, 1280
- **Default**: 640
- **Description**: Input image size (width/height) for the model
- **Use Case**: Match your inference requirements
  - 640: Standard YOLO detection
  - 1280: High-resolution detection
  - 320: Fast inference for real-time applications

### 2. **Batch Size** (batch)
- **UI Element**: Spin box
- **Range**: 1-128
- **Default**: 1
- **Description**: Number of images to process simultaneously
- **Use Case**: 
  - Batch=1: Single image inference (webcam, real-time)
  - Batch=8-32: Video processing, batch inference
  - Batch=64+: High-throughput server applications

### 3. **Export Format**
- **UI Element**: Dropdown menu
- **Options**: 
  - **TensorRT**: Optimized for NVIDIA GPUs
  - **ONNX**: Cross-platform compatibility
  - **TorchScript**: PyTorch native format
  - **OpenVINO**: Intel optimization
- **Default**: TensorRT
- **Description**: Target export format
- **Use Case**:
  - TensorRT: Maximum performance on NVIDIA GPUs
  - ONNX: Deployment on non-NVIDIA hardware
  - TorchScript: Pure PyTorch deployment
  - OpenVINO: Intel CPU/GPU optimization

### 4. **Device Selection**
- **UI Element**: Dropdown menu
- **Options**: 
  - 0 (GPU) - Primary GPU
  - 1 (GPU) - Secondary GPU
  - 2 (GPU) - Third GPU
  - 3 (GPU) - Fourth GPU
  - CPU - CPU execution
- **Default**: 0 (GPU)
- **Description**: Device to use for export process
- **Use Case**:
  - Multi-GPU systems: Select specific GPU
  - Testing: Export on CPU if no GPU available

## Updated Output Naming

Output files now include relevant parameters in the filename:

### TensorRT Engine
```
{model_name}_{precision}_b{batch}_img{imgsz}.engine
```
Example: `yolo11m_fp16_b32_img640.engine`

### ONNX
```
{model_name}_b{batch}_img{imgsz}.onnx
```
Example: `yolo11m_b32_img640.onnx`

### TorchScript
```
{model_name}_b{batch}_img{imgsz}.torchscript
```
Example: `yolo11m_b32_img640.torchscript`

### OpenVINO
```
{model_name}_b{batch}_img{imgsz}_openvino_model/
```
Example: `yolo11m_b32_img640_openvino_model/`

## Implementation Details

### Ultralytics YOLO Export
For PyTorch YOLO models (.pt, .pth), the application uses Ultralytics' native export:

```python
from ultralytics import YOLO

model = YOLO("models/yolo11m.pt")
model.export(
    format='engine',           # or 'onnx', 'torchscript', 'openvino'
    half=True,                 # FP16 precision
    imgsz=640,                 # Image size
    batch=32,                  # Batch size
    device=0                   # GPU device
)
```

### Fallback Mechanism
If Ultralytics export fails, the application falls back to manual conversion using the existing TensorRT converter.

## UI Enhancements

### Settings Panel Layout
```
Conversion Settings
├── Precision:          [FP32 ▼]
├── Image Size:         [640 ▼]
├── Batch Size:         [1 ⬆⬇]
├── Export Format:      [TensorRT ▼]
├── Device:             [0 (GPU) ▼]
├── Workspace Size:     [4 ⬆⬇] GB
└── Output Directory:   [Browse...]
```

### Conversion Progress Display
Shows all settings before starting:
```
Starting conversion with settings:
  - Format: TENSORRT
  - Precision: FP16
  - Image Size: 640
  - Batch Size: 32
  - Device: 0
  - Workspace: 4 GB

Loading YOLO model...
Exporting to TensorRT...
```

## Example Use Cases

### 1. High-Throughput Server
```
Image Size: 640
Batch Size: 32
Format: TensorRT
Precision: FP16
Device: 0 (GPU)
```
**Result**: Optimized for processing 32 images simultaneously

### 2. Real-Time Detection
```
Image Size: 640
Batch Size: 1
Format: TensorRT
Precision: FP16
Device: 0 (GPU)
```
**Result**: Low latency for webcam/video stream

### 3. High-Resolution Detection
```
Image Size: 1280
Batch Size: 8
Format: TensorRT
Precision: FP16
Device: 0 (GPU)
```
**Result**: Better accuracy for small objects

### 4. Edge Deployment (CPU)
```
Image Size: 320
Batch Size: 1
Format: ONNX
Precision: FP32
Device: CPU
```
**Result**: CPU-optimized for edge devices

### 5. Cross-Platform
```
Image Size: 640
Batch Size: 1
Format: ONNX
Precision: FP32
Device: 0 (GPU)
```
**Result**: ONNX for deployment on any platform

## Benefits

### 1. **Flexibility**
- Export to multiple formats from one interface
- Configure for specific use cases
- Support multi-GPU systems

### 2. **Traceability**
- Filenames include configuration
- Easy to identify model variants
- No confusion about model settings

### 3. **Performance Optimization**
- Batch size tuning for throughput
- Image size matching for accuracy
- Device selection for multi-GPU

### 4. **Professional Workflow**
- Industry-standard parameters
- Matches Ultralytics API
- Compatible with deployment pipelines

## Testing Checklist

- [ ] Test with different image sizes (320, 640, 1280)
- [ ] Test with different batch sizes (1, 8, 32)
- [ ] Test all export formats (TensorRT, ONNX, TorchScript, OpenVINO)
- [ ] Test different precisions (FP32, FP16, INT8)
- [ ] Test device selection (GPU 0, GPU 1, CPU)
- [ ] Verify output file naming
- [ ] Test with YOLO models
- [ ] Test with custom PyTorch models
- [ ] Test with ONNX models

## Future Enhancements

### Potential Additions
1. **Dynamic Shape Support**: Min/Max/Optimal shapes for TensorRT
2. **Quantization Options**: PTQ/QAT settings for INT8
3. **Profile Selection**: Optimize for latency vs throughput
4. **Multi-Input Support**: Multiple input sizes in one engine
5. **Workspace Presets**: Common configurations (edge, server, cloud)
6. **Export Presets**: Quick buttons for common scenarios
7. **Model Analysis**: Show expected performance/memory usage
8. **Batch Testing**: Export multiple configurations at once

## Migration Notes

### For Existing Users
- All previous functionality preserved
- New parameters have sensible defaults
- Existing conversions will work as before
- Output naming changed (includes parameters now)

### For Developers
- `ConversionWorker` updated with new parameters
- Settings section reorganized with new controls
- Ultralytics export integrated as primary method
- Fallback to manual conversion still available

---

**Last Updated**: October 22, 2025  
**Version**: 1.1.0  
**Status**: ✅ Implemented and tested
