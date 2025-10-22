"""
Configuration settings for the TensorRT Model Converter application.
"""
import os
from pathlib import Path

# Application metadata
APP_NAME = "TensorRT Model Converter"
APP_VERSION = "1.0.0"

# Paths
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

# Create necessary directories
LOGS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Supported model formats
SUPPORTED_INPUT_FORMATS = [
    ".onnx",
    ".pt",
    ".pth",
    ".pb",
    ".tflite"
]

# TensorRT settings
DEFAULT_PRECISION = "fp16"  # Options: fp32, fp16, int8
SUPPORTED_PRECISIONS = ["fp32", "fp16", "int8"]

# Default workspace size (in GB)
DEFAULT_WORKSPACE_SIZE = 4

# GUI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# Logging settings
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "converter.log"
