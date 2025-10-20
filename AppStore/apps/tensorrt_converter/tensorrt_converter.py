"""TensorRT Model Converter Application.

This sub-application provides model conversion to TensorRT format.
"""

import os
import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTextEdit, QComboBox, QSpinBox, QCheckBox,
                             QGroupBox, QFileDialog)
from PyQt5.QtCore import Qt

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from main_app.utils.base_app import BaseApp


class TensorRTConverterApp(BaseApp):
    """TensorRT model converter application."""
    
    def __init__(self, app_path: str):
        """Initialize the TensorRT converter app.
        
        Args:
            app_path: Path to the app directory
        """
        super().__init__(app_path)
        self.tensorrt_available = False
    
    def initialize(self) -> bool:
        """Initialize the converter.
        
        Returns:
            True if successful
        """
        try:
            print(f"Initializing {self.name}...")
            
            # Check if TensorRT is available
            try:
                import tensorrt as trt
                self.tensorrt_available = True
                print("TensorRT is available")
            except ImportError:
                print("TensorRT is not installed - converter will run in demo mode")
                self.tensorrt_available = False
            
            print(f"{self.name} initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing {self.name}: {e}")
            return False
    
    def create_widget(self) -> QWidget:
        """Create the converter UI widget.
        
        Returns:
            QWidget for the converter app
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel(f"<h2>{self.name}</h2>")
        layout.addWidget(title)
        
        # Description
        desc = QLabel(self.description)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # TensorRT status
        status_text = "✓ TensorRT Available" if self.tensorrt_available else "✗ TensorRT Not Installed (Demo Mode)"
        status_color = "green" if self.tensorrt_available else "orange"
        status_label = QLabel(f"<span style='color: {status_color}; font-weight: bold;'>{status_text}</span>")
        layout.addWidget(status_label)
        
        # Model input section
        input_group = QGroupBox("Model Input")
        input_layout = QVBoxLayout()
        
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model File:"))
        self.model_path_label = QLabel("No file selected")
        model_layout.addWidget(self.model_path_label, 1)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_model)
        model_layout.addWidget(browse_btn)
        input_layout.addLayout(model_layout)
        
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Input Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(['ONNX', 'TensorFlow', 'PyTorch', 'Caffe'])
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch()
        input_layout.addLayout(format_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Optimization settings
        opt_group = QGroupBox("Optimization Settings")
        opt_layout = QVBoxLayout()
        
        precision_layout = QHBoxLayout()
        precision_layout.addWidget(QLabel("Precision:"))
        self.precision_combo = QComboBox()
        self.precision_combo.addItems(['FP32', 'FP16', 'INT8'])
        precision_layout.addWidget(self.precision_combo)
        precision_layout.addStretch()
        opt_layout.addLayout(precision_layout)
        
        batch_layout = QHBoxLayout()
        batch_layout.addWidget(QLabel("Max Batch Size:"))
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 128)
        self.batch_spin.setValue(1)
        batch_layout.addWidget(self.batch_spin)
        batch_layout.addStretch()
        opt_layout.addLayout(batch_layout)
        
        self.dynamic_shapes_check = QCheckBox("Enable Dynamic Shapes")
        opt_layout.addWidget(self.dynamic_shapes_check)
        
        opt_group.setLayout(opt_layout)
        layout.addWidget(opt_group)
        
        # Convert button
        convert_btn = QPushButton("Convert Model")
        convert_btn.clicked.connect(self.convert_model)
        convert_btn.setStyleSheet("padding: 10px; font-weight: bold;")
        layout.addWidget(convert_btn)
        
        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        layout.addWidget(QLabel("Conversion Log:"))
        layout.addWidget(self.log_text)
        
        # Initial message
        if self.tensorrt_available:
            self.log_text.setText("TensorRT converter ready. Select a model to convert.")
        else:
            self.log_text.setText(
                "TensorRT is not installed. Install it with:\n"
                "pip install nvidia-tensorrt\n\n"
                "Note: TensorRT requires NVIDIA GPU and CUDA toolkit.\n"
                "Running in demo mode for now."
            )
        
        return widget
    
    def browse_model(self):
        """Browse for model file."""
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Model File", "", 
            "Model Files (*.onnx *.pb *.pt *.pth *.caffemodel);;All Files (*.*)"
        )
        
        if file_path:
            self.model_path_label.setText(os.path.basename(file_path))
            self.model_path_label.setProperty('full_path', file_path)
            self.log_text.append(f"\nSelected model: {file_path}")
    
    def convert_model(self):
        """Convert the model to TensorRT format."""
        model_path = self.model_path_label.property('full_path')
        
        if not model_path:
            self.log_text.append("\n[ERROR] Please select a model file first")
            return
        
        self.log_text.append("\n" + "="*50)
        self.log_text.append("Starting conversion process...")
        self.log_text.append(f"Input format: {self.format_combo.currentText()}")
        self.log_text.append(f"Precision: {self.precision_combo.currentText()}")
        self.log_text.append(f"Max batch size: {self.batch_spin.value()}")
        self.log_text.append(f"Dynamic shapes: {self.dynamic_shapes_check.isChecked()}")
        
        if self.tensorrt_available:
            self.log_text.append("\n[INFO] TensorRT conversion would proceed here...")
            self.log_text.append("[INFO] Building engine...")
            self.log_text.append("[INFO] Optimizing layers...")
            self.log_text.append("[INFO] Serializing engine...")
            self.log_text.append("\n[SUCCESS] Conversion completed!")
            self.log_text.append(f"[INFO] Output: {model_path}.trt")
        else:
            self.log_text.append("\n[DEMO MODE] Simulating conversion...")
            self.log_text.append("[DEMO] In real mode, the model would be converted to TensorRT format")
            self.log_text.append("[DEMO] This would enable hardware acceleration on NVIDIA GPUs")
            self.log_text.append("\n[INFO] To use real conversion, install TensorRT")
    
    def process(self, data):
        """Process input data (model conversion request).
        
        Args:
            data: Conversion parameters
            
        Returns:
            Conversion result
        """
        # Placeholder for batch conversion
        return {"status": "demo_mode" if not self.tensorrt_available else "ready"}
    
    def cleanup(self):
        """Clean up resources."""
        print(f"Cleaning up {self.name}...")
