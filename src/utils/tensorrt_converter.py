"""
TensorRT model converter module.
Handles conversion of models (ONNX, PyTorch, etc.) to TensorRT engine format.
"""
import os
from pathlib import Path
from typing import Optional, Callable
import numpy as np

from src.utils.logger import setup_logger
from src.utils.hardware_detector import HardwareInfo

logger = setup_logger(__name__)


class TensorRTConverter:
    """Converter for optimizing models to TensorRT engine format."""
    
    def __init__(self, hardware_info: HardwareInfo):
        """
        Initialize the TensorRT converter.
        
        Args:
            hardware_info: Hardware information for optimization
        """
        self.hardware_info = hardware_info
        self.logger = logger
        
        # Check TensorRT availability
        if not hardware_info.has_tensorrt:
            raise RuntimeError("TensorRT is not available on this system")
        
        import tensorrt as trt
        self.trt = trt
        self.TRT_LOGGER = trt.Logger(trt.Logger.INFO)
    
    def convert_onnx_to_engine(
        self,
        onnx_path: str,
        engine_path: str,
        precision: str = "fp16",
        workspace_size: int = 4,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        Convert ONNX model to TensorRT engine.
        
        Args:
            onnx_path: Path to input ONNX model
            engine_path: Path to output TensorRT engine
            precision: Precision mode ('fp32', 'fp16', 'int8')
            workspace_size: Workspace size in GB
            progress_callback: Optional callback for progress updates
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            self._update_progress(progress_callback, "Initializing TensorRT builder...")
            
            # Create builder and network
            builder = self.trt.Builder(self.TRT_LOGGER)
            network = builder.create_network(
                1 << int(self.trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
            )
            parser = self.trt.OnnxParser(network, self.TRT_LOGGER)
            
            # Parse ONNX model
            self._update_progress(progress_callback, f"Parsing ONNX model: {Path(onnx_path).name}")
            self.logger.info(f"Loading ONNX model from {onnx_path}")
            
            with open(onnx_path, 'rb') as model_file:
                if not parser.parse(model_file.read()):
                    self.logger.error("Failed to parse ONNX model")
                    for error in range(parser.num_errors):
                        self.logger.error(parser.get_error(error))
                    return False
            
            self._update_progress(progress_callback, "Configuring builder...")
            
            # Configure builder
            config = builder.create_builder_config()
            
            # Set workspace size
            workspace_bytes = workspace_size * (1 << 30)  # Convert GB to bytes
            config.set_memory_pool_limit(
                self.trt.MemoryPoolType.WORKSPACE, 
                workspace_bytes
            )
            
            # Set precision
            self._update_progress(progress_callback, f"Setting precision mode: {precision.upper()}")
            if precision.lower() == "fp16" and builder.platform_has_fast_fp16:
                config.set_flag(self.trt.BuilderFlag.FP16)
                self.logger.info("FP16 mode enabled")
            elif precision.lower() == "int8" and builder.platform_has_fast_int8:
                config.set_flag(self.trt.BuilderFlag.INT8)
                self.logger.info("INT8 mode enabled (requires calibration)")
                # Note: INT8 requires calibration data, which is not implemented here
            else:
                self.logger.info("FP32 mode enabled")
            
            # Build engine
            self._update_progress(progress_callback, "Building TensorRT engine (this may take a while)...")
            self.logger.info("Building TensorRT engine...")
            
            serialized_engine = builder.build_serialized_network(network, config)
            
            if serialized_engine is None:
                self.logger.error("Failed to build TensorRT engine")
                return False
            
            # Save engine
            self._update_progress(progress_callback, f"Saving engine to: {Path(engine_path).name}")
            self.logger.info(f"Saving engine to {engine_path}")
            
            with open(engine_path, 'wb') as f:
                f.write(serialized_engine)
            
            self._update_progress(progress_callback, "Conversion completed successfully!")
            self.logger.info(f"Engine saved successfully to {engine_path}")
            
            # Get engine size
            engine_size_mb = os.path.getsize(engine_path) / (1024 * 1024)
            self.logger.info(f"Engine size: {engine_size_mb:.2f} MB")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during conversion: {e}", exc_info=True)
            self._update_progress(progress_callback, f"Error: {str(e)}")
            return False
    
    def convert_pytorch_to_engine(
        self,
        pytorch_path: str,
        engine_path: str,
        input_shape: tuple = (1, 3, 640, 640),
        precision: str = "fp16",
        workspace_size: int = 4,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> bool:
        """
        Convert PyTorch model to TensorRT engine via ONNX.
        
        Args:
            pytorch_path: Path to PyTorch model (.pt or .pth)
            engine_path: Path to output TensorRT engine
            input_shape: Input tensor shape (batch, channels, height, width), default (1, 3, 640, 640)
            precision: Precision mode ('fp32', 'fp16', 'int8')
            workspace_size: Workspace size in GB
            progress_callback: Optional callback for progress updates
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            import torch
            
            # Try to use Ultralytics for YOLO models first (more reliable)
            try:
                from ultralytics import YOLO
                
                self._update_progress(progress_callback, "Detected YOLO model, using Ultralytics...")
                self.logger.info(f"Loading YOLO model from {pytorch_path}")
                
                yolo_model = YOLO(pytorch_path)
                
                # Export to ONNX first
                onnx_path = engine_path.replace('.engine', '.onnx')
                self._update_progress(progress_callback, "Exporting YOLO model to ONNX...")
                
                yolo_model.export(
                    format='onnx',
                    imgsz=input_shape[2],  # Use height from input_shape
                    dynamic=False,
                    simplify=True
                )
                
                # The exported file will be next to the .pt file
                import os
                base_name = os.path.splitext(pytorch_path)[0]
                exported_onnx = f"{base_name}.onnx"
                
                if os.path.exists(exported_onnx):
                    # Convert ONNX to TensorRT
                    result = self.convert_onnx_to_engine(
                        exported_onnx,
                        engine_path,
                        precision,
                        workspace_size,
                        progress_callback
                    )
                    
                    # Clean up temporary ONNX file if requested
                    if result and exported_onnx != onnx_path:
                        import shutil
                        try:
                            shutil.move(exported_onnx, onnx_path)
                            self.logger.info(f"Moved ONNX file to: {onnx_path}")
                        except:
                            pass
                    
                    return result
                else:
                    self.logger.warning("Ultralytics export failed, trying manual conversion...")
                    
            except ImportError:
                self.logger.info("Ultralytics not used, falling back to manual PyTorch conversion...")
            except Exception as e:
                self.logger.warning(f"YOLO export failed: {e}, trying manual conversion...")
            
            # Fallback: Manual PyTorch conversion
            self._update_progress(progress_callback, "Loading PyTorch model...")
            self.logger.info(f"Loading PyTorch model from {pytorch_path}")
            
            # Load PyTorch model
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            # PyTorch 2.6+ requires weights_only=False for models with custom classes
            # This is safe for trusted model files (like YOLO models you trained)
            model = torch.load(pytorch_path, map_location=device, weights_only=False)
            
            # Handle different model formats
            if isinstance(model, dict):
                if 'model' in model:
                    model = model['model']
                elif 'ema' in model:
                    model = model['ema']
                else:
                    self.logger.warning("Model checkpoint structure not recognized, trying to use as-is")
            
            # Handle YOLO models - extract the model if it's wrapped
            if hasattr(model, 'model'):
                model = model.model
            
            model.eval()
            model.to(device)
            
            # Create temporary ONNX file
            onnx_path = engine_path.replace('.engine', '.onnx')
            
            self._update_progress(progress_callback, "Exporting to ONNX...")
            self.logger.info(f"Exporting to ONNX format: {onnx_path}")
            
            # Create dummy input
            dummy_input = torch.randn(*input_shape).to(device)
            
            # Export to ONNX
            torch.onnx.export(
                model,
                dummy_input,
                onnx_path,
                input_names=['input'],
                output_names=['output'],
                dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}},
                opset_version=12
            )
            
            # Convert ONNX to TensorRT
            result = self.convert_onnx_to_engine(
                onnx_path,
                engine_path,
                precision,
                workspace_size,
                progress_callback
            )
            
            # Clean up temporary ONNX file
            if os.path.exists(onnx_path):
                os.remove(onnx_path)
                self.logger.info("Temporary ONNX file removed")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error converting PyTorch model: {e}", exc_info=True)
            self._update_progress(progress_callback, f"Error: {str(e)}")
            return False
    
    def _update_progress(
        self,
        callback: Optional[Callable[[str], None]],
        message: str
    ):
        """Update progress via callback if provided."""
        if callback:
            callback(message)
        self.logger.info(message)
    
    def validate_model(self, model_path: str) -> tuple[bool, str]:
        """
        Validate if the model file is supported and accessible.
        
        Args:
            model_path: Path to model file
            
        Returns:
            Tuple of (is_valid, message)
        """
        path = Path(model_path)
        
        if not path.exists():
            return False, "File does not exist"
        
        if not path.is_file():
            return False, "Path is not a file"
        
        extension = path.suffix.lower()
        
        if extension == '.onnx':
            return True, "ONNX model detected"
        elif extension in ['.pt', '.pth']:
            return True, "PyTorch model detected"
        elif extension == '.engine':
            return False, "File is already a TensorRT engine"
        else:
            return False, f"Unsupported file format: {extension}"
