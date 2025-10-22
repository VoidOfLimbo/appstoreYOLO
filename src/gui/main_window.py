"""
Main GUI application for TensorRT Model Converter.
"""
import sys
import shutil
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QGroupBox,
    QFileDialog, QSpinBox, QProgressBar, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QFont

from src.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    SUPPORTED_PRECISIONS, DEFAULT_PRECISION, DEFAULT_WORKSPACE_SIZE,
    OUTPUT_DIR
)
from src.utils.hardware_detector import HardwareDetector, HardwareInfo
from src.utils.tensorrt_converter import TensorRTConverter
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ConversionWorker(QThread):
    """Worker thread for model conversion to avoid blocking the GUI."""
    
    progress = pyqtSignal(str)
    progress_percent = pyqtSignal(int)  # Signal for progress bar percentage
    finished = pyqtSignal(bool, str)
    
    def __init__(
        self,
        converter: TensorRTConverter,
        model_path: str,
        output_path: str,
        precision: str,
        workspace_size: int,
        imgsz: int = 640,
        batch: int = 32,
        export_format: str = 'tensorrt',
        device: int = 0,
        simplify: bool = False,
        use_default_location: bool = False
    ):
        super().__init__()
        self.converter = converter
        self.model_path = model_path
        self.output_path = output_path
        self.precision = precision
        self.workspace_size = workspace_size
        self.imgsz = imgsz
        self.batch = batch
        self.export_format = export_format
        self.device = device
        self.simplify = simplify
        self.use_default_location = use_default_location
    
    def run(self):
        """Run the conversion in a separate thread."""
        try:
            model_ext = Path(self.model_path).suffix.lower()
            
            # Check if it's a YOLO model and use Ultralytics export
            if model_ext in ['.pt', '.pth']:
                try:
                    from ultralytics import YOLO
                    
                    self.progress_percent.emit(10)
                    self.progress.emit(f"Loading YOLO model: {self.model_path}")
                    model = YOLO(self.model_path)
                    
                    self.progress_percent.emit(20)
                    self.progress.emit(f"\nExporting to {self.export_format.upper()}...")
                    self.progress.emit(f"Settings: imgsz={self.imgsz}, batch={self.batch}, device={self.device}\n")
                    
                    # Map format names
                    format_map = {
                        'tensorrt': 'engine',
                        'onnx': 'onnx',
                        'torchscript': 'torchscript',
                        'openvino': 'openvino'
                    }
                    
                    self.progress_percent.emit(30)
                    # Export with Ultralytics
                    result = model.export(
                        format=format_map.get(self.export_format, 'engine'),
                        half=(self.precision == 'fp16'),
                        imgsz=self.imgsz,
                        batch=self.batch,
                        device=self.device,
                        simplify=self.simplify  # ONNX graph simplification (can crash on Windows)
                    )
                    
                    self.progress_percent.emit(90)
                    self.progress.emit(f"\n✅ Export completed successfully!")
                    
                    # Find the file created by Ultralytics (in the model's directory)
                    model_dir = Path(self.model_path).parent
                    model_stem = Path(self.model_path).stem
                    
                    # Ultralytics creates files with specific naming in the model directory
                    if self.export_format == 'tensorrt':
                        ultralytics_output = model_dir / f"{model_stem}.engine"
                    elif self.export_format == 'onnx':
                        ultralytics_output = model_dir / f"{model_stem}.onnx"
                    elif self.export_format == 'torchscript':
                        ultralytics_output = model_dir / f"{model_stem}.torchscript"
                    else:  # openvino
                        ultralytics_output = model_dir / f"{model_stem}_openvino_model"
                    
                    # Move the file to the desired output directory (if not using default location)
                    final_output = Path(self.output_path)
                    
                    if self.use_default_location:
                        # Keep the file in the default location (same as model)
                        self.progress_percent.emit(95)
                        self.progress.emit(f"File saved in default location: {ultralytics_output}")
                        actual_output = ultralytics_output
                    elif ultralytics_output.exists() and ultralytics_output != final_output:
                        # Move to custom output directory
                        self.progress_percent.emit(95)
                        self.progress.emit(f"Moving output to: {final_output}")
                        
                        # For OpenVINO, it's a directory
                        if self.export_format == 'openvino' and ultralytics_output.is_dir():
                            if final_output.exists():
                                shutil.rmtree(final_output)
                            shutil.move(str(ultralytics_output), str(final_output))
                        else:
                            # For file outputs
                            shutil.move(str(ultralytics_output), str(final_output))
                        
                        actual_output = final_output
                    elif ultralytics_output.exists():
                        # File is already in the right place
                        actual_output = ultralytics_output
                    else:
                        self.progress.emit(f"Warning: Could not find output at {ultralytics_output}")
                        actual_output = ultralytics_output
                    
                    self.progress_percent.emit(100)
                    success = True
                    message = (
                        f"Conversion completed successfully!\n\n"
                        f"Output saved to:\n{actual_output}\n\n"
                        f"Format: {self.export_format.upper()}\n"
                        f"Precision: {self.precision.upper()}\n"
                        f"Image Size: {self.imgsz}\n"
                        f"Batch Size: {self.batch}"
                    )
                    self.finished.emit(True, message)
                    return
                    
                except Exception as e:
                    self.progress.emit(f"Ultralytics export failed: {str(e)}")
                    self.progress.emit("Falling back to manual conversion...")
                    
                    # Fallback to manual conversion
                    input_shape = (self.batch, 3, self.imgsz, self.imgsz)
                    success = self.converter.convert_pytorch_to_engine(
                        self.model_path,
                        self.output_path,
                        input_shape=input_shape,
                        precision=self.precision,
                        workspace_size=self.workspace_size,
                        progress_callback=self.progress.emit
                    )
            
            elif model_ext == '.onnx':
                self.progress.emit("Converting ONNX model to TensorRT...")
                success = self.converter.convert_onnx_to_engine(
                    self.model_path,
                    self.output_path,
                    self.precision,
                    self.workspace_size,
                    progress_callback=self.progress.emit
                )
            else:
                success = False
                message = f"Unsupported file format: {model_ext}"
                self.finished.emit(False, message)
                return
            
            if success:
                message = f"Conversion completed successfully!\nOutput saved to: {self.output_path}"
            else:
                message = "Conversion failed. Check the log for details."
            
            self.finished.emit(success, message)
            
        except Exception as e:
            logger.error(f"Error in conversion worker: {e}", exc_info=True)
            self.finished.emit(False, f"Error: {str(e)}")


class DropZone(QLabel):
    """Custom label widget that accepts drag and drop."""
    
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f0f0f0;
                padding: 20px;
                font-size: 14px;
                color: #666;
            }
            QLabel:hover {
                border-color: #0078d4;
                background-color: #e8f4fd;
            }
        """)
        self.setText("Drag & Drop model file here\n\nor\n\nClick 'Browse' button")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    border: 2px solid #0078d4;
                    border-radius: 10px;
                    background-color: #cce8ff;
                    padding: 20px;
                    font-size: 14px;
                    color: #0078d4;
                }
            """)
    
    def dragLeaveEvent(self, event):
        """Handle drag leave event."""
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f0f0f0;
                padding: 20px;
                font-size: 14px;
                color: #666;
            }
            QLabel:hover {
                border-color: #0078d4;
                background-color: #e8f4fd;
            }
        """)
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.file_dropped.emit(files[0])
        
        self.dragLeaveEvent(event)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.hardware_info: Optional[HardwareInfo] = None
        self.converter: Optional[TensorRTConverter] = None
        self.worker: Optional[ConversionWorker] = None
        self.model_path: Optional[str] = None
        
        self.init_ui()
        self.detect_hardware()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Title
        title_label = QLabel("TensorRT Model Converter")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Hardware info and settings side-by-side
        info_settings_layout = QHBoxLayout()
        
        # Hardware info section (left)
        self.hardware_group = self.create_hardware_info_section()
        info_settings_layout.addWidget(self.hardware_group)
        
        # Conversion settings section (right)
        settings_group = self.create_settings_section()
        info_settings_layout.addWidget(settings_group)
        
        main_layout.addLayout(info_settings_layout)
        
        # File selection section
        file_group = self.create_file_selection_section()
        main_layout.addWidget(file_group)
        
        # Progress section
        progress_group = self.create_progress_section()
        main_layout.addWidget(progress_group)
        
        # Convert button
        self.convert_button = QPushButton("Export Model")
        self.convert_button.setEnabled(False)
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.convert_button.clicked.connect(self.start_conversion)
        main_layout.addWidget(self.convert_button)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_hardware_info_section(self) -> QGroupBox:
        """Create hardware information section."""
        group = QGroupBox("Hardware Information")
        layout = QVBoxLayout()
        
        self.hardware_text = QTextEdit()
        self.hardware_text.setReadOnly(True)
        self.hardware_text.setMinimumHeight(180)
        self.hardware_text.setText("Detecting hardware...")
        
        layout.addWidget(self.hardware_text)
        group.setLayout(layout)
        
        return group
    
    def create_file_selection_section(self) -> QGroupBox:
        """Create file selection section."""
        group = QGroupBox("Model Selection")
        layout = QVBoxLayout()
        
        # Browse button and file path
        browse_layout = QHBoxLayout()
        
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("No file selected")
        self.file_path_edit.setReadOnly(True)
        browse_layout.addWidget(self.file_path_edit)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_file)
        browse_layout.addWidget(browse_button)
        
        layout.addLayout(browse_layout)
        
        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.file_dropped.connect(self.on_file_dropped)
        layout.addWidget(self.drop_zone)
        group.setLayout(layout)
        
        return group
    
    def create_settings_section(self) -> QGroupBox:
        """Create conversion settings section."""
        group = QGroupBox("Conversion Settings")
        layout = QVBoxLayout()
        
        # Precision setting
        precision_layout = QHBoxLayout()
        precision_layout.addWidget(QLabel("Precision:"))
        
        self.precision_combo = QComboBox()
        self.precision_combo.addItems([p.upper() for p in SUPPORTED_PRECISIONS])
        self.precision_combo.setCurrentText(DEFAULT_PRECISION.upper())
        precision_layout.addWidget(self.precision_combo)
        
        layout.addLayout(precision_layout)
        
        # Image size setting
        imgsz_layout = QHBoxLayout()
        imgsz_layout.addWidget(QLabel("Image Size:"))
        
        self.imgsz_combo = QComboBox()
        self.imgsz_combo.addItems(["320", "416", "512", "640", "800", "1024", "1280"])
        self.imgsz_combo.setCurrentText("640")
        self.imgsz_combo.setToolTip("Input image size for the model (width/height)")
        imgsz_layout.addWidget(self.imgsz_combo)
        
        layout.addLayout(imgsz_layout)
        
        # Batch size setting
        batch_layout = QHBoxLayout()
        batch_layout.addWidget(QLabel("Batch Size:"))
        
        self.batch_spin = QSpinBox()
        self.batch_spin.setMinimum(1)
        self.batch_spin.setMaximum(128)
        self.batch_spin.setValue(32)
        self.batch_spin.setToolTip("Number of images to process simultaneously\nRecommended: 1 for real-time, 8-32 for batch processing")
        batch_layout.addWidget(self.batch_spin)
        
        layout.addLayout(batch_layout)
        
        # Export format setting
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Export Format:"))
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["TensorRT", "ONNX", "TorchScript", "OpenVINO"])
        self.format_combo.setCurrentText("TensorRT")
        self.format_combo.setToolTip("Target export format")
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        format_layout.addWidget(self.format_combo)
        
        layout.addLayout(format_layout)
        
        # Device selection
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("Device:"))
        
        self.device_combo = QComboBox()
        self.device_combo.addItems(["0 (GPU)", "1 (GPU)", "2 (GPU)", "3 (GPU)", "cpu"])
        self.device_combo.setCurrentText("0 (GPU)")
        self.device_combo.setToolTip("Device to use for export (GPU index or CPU)")
        device_layout.addWidget(self.device_combo)
        
        layout.addLayout(device_layout)
        
        # Workspace size setting
        workspace_layout = QHBoxLayout()
        workspace_layout.addWidget(QLabel("Workspace Size (GB):"))
        
        self.workspace_spin = QSpinBox()
        self.workspace_spin.setMinimum(1)
        self.workspace_spin.setMaximum(16)
        self.workspace_spin.setValue(DEFAULT_WORKSPACE_SIZE)
        self.workspace_spin.setToolTip("Maximum GPU memory workspace for TensorRT")
        workspace_layout.addWidget(self.workspace_spin)
        
        layout.addLayout(workspace_layout)
        
        # Checkboxes side by side
        checkboxes_layout = QHBoxLayout()
        
        # Simplify ONNX checkbox
        self.simplify_check = QCheckBox("Simplify ONNX (Advanced)")
        self.simplify_check.setChecked(False)
        self.simplify_check.setToolTip(
            "Enable ONNX graph simplification using onnxslim.\n"
            "Makes model smaller but may crash on Windows.\n"
            "Leave unchecked unless you need it."
        )
        checkboxes_layout.addWidget(self.simplify_check)
        
        # Default export location checkbox
        self.default_location_check = QCheckBox("Use Default Export Location")
        self.default_location_check.setChecked(True)
        self.default_location_check.setToolTip(
            "Export file to the same directory as the source model.\n"
            "When unchecked, exports to the directory specified below."
        )
        self.default_location_check.stateChanged.connect(self.on_default_location_changed)
        checkboxes_layout.addWidget(self.default_location_check)
        
        layout.addLayout(checkboxes_layout)
        
        # Output path
        output_label = QLabel("Output Directory:")
        layout.addWidget(output_label)
        
        output_path_layout = QHBoxLayout()
        
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setText(str(OUTPUT_DIR))
        self.output_path_edit.setEnabled(False)  # Disabled by default since "Use Default Location" is checked
        output_path_layout.addWidget(self.output_path_edit)
        
        self.output_browse_button = QPushButton("Browse...")
        self.output_browse_button.clicked.connect(self.browse_output_dir)
        self.output_browse_button.setEnabled(False)  # Disabled by default since "Use Default Location" is checked
        output_path_layout.addWidget(self.output_browse_button)
        
        layout.addLayout(output_path_layout)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        group.setLayout(layout)
        
        return group
    
    def create_progress_section(self) -> QGroupBox:
        """Create progress section."""
        group = QGroupBox("Conversion Progress")
        layout = QVBoxLayout()
        
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setMaximumHeight(120)
        
        layout.addWidget(self.progress_text)
        
        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        layout.addWidget(self.progress_bar)
        
        group.setLayout(layout)
        
        return group
    
    def detect_hardware(self):
        """Detect hardware capabilities."""
        try:
            detector = HardwareDetector()
            self.hardware_info = detector.detect()
            
            # Update hardware info display
            summary = detector.get_summary(self.hardware_info)
            self.hardware_text.setText(summary)
            
            # Set recommended precision
            recommended = self.hardware_info.recommended_precision.upper()
            self.precision_combo.setCurrentText(recommended)
            
            # Initialize converter if TensorRT is available
            if self.hardware_info.has_tensorrt:
                self.converter = TensorRTConverter(self.hardware_info)
                self.statusBar().showMessage("Hardware detected successfully. Ready to convert models.")
            else:
                self.statusBar().showMessage("Warning: TensorRT not available. Conversion disabled.")
                QMessageBox.warning(
                    self,
                    "TensorRT Not Available",
                    "TensorRT is not installed or not available on this system.\n"
                    "Please install TensorRT to use this application."
                )
            
        except Exception as e:
            logger.error(f"Error detecting hardware: {e}", exc_info=True)
            self.hardware_text.setText(f"Error detecting hardware: {str(e)}")
            self.statusBar().showMessage("Hardware detection failed")
    
    def browse_file(self):
        """Open file browser dialog."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Model File",
            "",
            "Model Files (*.onnx *.pt *.pth);;All Files (*.*)"
        )
        
        if file_path:
            self.on_file_selected(file_path)
    
    def browse_output_dir(self):
        """Open directory browser dialog."""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            str(OUTPUT_DIR)
        )
        
        if dir_path:
            self.output_path_edit.setText(dir_path)
    
    def on_format_changed(self, format_text: str):
        """Handle export format change."""
        # Update button text based on format
        format_lower = format_text.lower()
        if format_lower == "tensorrt":
            self.convert_button.setText("Export to TensorRT")
        elif format_lower == "onnx":
            self.convert_button.setText("Export to ONNX")
        elif format_lower == "torchscript":
            self.convert_button.setText("Export to TorchScript")
        else:  # openvino
            self.convert_button.setText("Export to OpenVINO")
    
    def on_default_location_changed(self, state: int):
        """Handle default location checkbox change."""
        use_default = (state == 2)  # Qt.Checked = 2
        # Disable output directory controls when using default location
        self.output_path_edit.setEnabled(not use_default)
        self.output_browse_button.setEnabled(not use_default)
    
    def on_file_dropped(self, file_path: str):
        """Handle file drop event."""
        self.on_file_selected(file_path)
    
    def on_file_selected(self, file_path: str):
        """Handle file selection."""
        if not self.converter:
            QMessageBox.warning(
                self,
                "TensorRT Not Available",
                "TensorRT is not available. Cannot process models."
            )
            return
        
        # Validate model file
        is_valid, message = self.converter.validate_model(file_path)
        
        if is_valid:
            self.model_path = file_path
            self.file_path_edit.setText(file_path)
            self.convert_button.setEnabled(True)
            self.statusBar().showMessage(f"{message}: {Path(file_path).name}")
            self.drop_zone.setText(f"Selected: {Path(file_path).name}")
        else:
            self.model_path = None
            self.file_path_edit.setText("")
            self.convert_button.setEnabled(False)
            self.statusBar().showMessage(f"Invalid file: {message}")
            QMessageBox.warning(self, "Invalid File", message)
            self.drop_zone.setText("Drag & Drop model file here\n\nor\n\nClick 'Browse' button")
    
    def start_conversion(self):
        """Start the model conversion process."""
        if not self.model_path or not self.converter:
            return
        
        # Get settings
        precision = self.precision_combo.currentText().lower()
        workspace_size = self.workspace_spin.value()
        imgsz = int(self.imgsz_combo.currentText())
        batch = self.batch_spin.value()
        export_format = self.format_combo.currentText().lower()
        simplify = self.simplify_check.isChecked()
        use_default_location = self.default_location_check.isChecked()
        
        # Parse device (extract number or 'cpu')
        device_text = self.device_combo.currentText()
        if 'cpu' in device_text.lower():
            device = 'cpu'
        else:
            device = int(device_text.split()[0])
        
        # Determine output directory
        if use_default_location:
            # Use the same directory as the model
            output_dir = Path(self.model_path).parent
        else:
            # Use the specified output directory
            output_dir = Path(self.output_path_edit.text())
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output file path based on format
        model_name = Path(self.model_path).stem
        if export_format == "tensorrt":
            output_path = output_dir / f"{model_name}_{precision}_b{batch}_img{imgsz}.engine"
        elif export_format == "onnx":
            output_path = output_dir / f"{model_name}_b{batch}_img{imgsz}.onnx"
        elif export_format == "torchscript":
            output_path = output_dir / f"{model_name}_b{batch}_img{imgsz}.torchscript"
        else:  # openvino
            output_path = output_dir / f"{model_name}_b{batch}_img{imgsz}_openvino_model"
        
        # Disable UI during conversion
        self.convert_button.setEnabled(False)
        self.statusBar().showMessage("Converting...")
        self.progress_text.clear()
        self.progress_bar.setValue(0)
        self.progress_text.append(f"Starting conversion with settings:\n")
        self.progress_text.append(f"  - Format: {export_format.upper()}\n")
        self.progress_text.append(f"  - Precision: {precision.upper()}\n")
        self.progress_text.append(f"  - Image Size: {imgsz}\n")
        self.progress_text.append(f"  - Batch Size: {batch}\n")
        self.progress_text.append(f"  - Device: {device}\n")
        self.progress_text.append(f"  - Workspace: {workspace_size} GB\n")
        self.progress_text.append(f"  - Simplify ONNX: {'Yes' if simplify else 'No'}\n")
        self.progress_text.append(f"  - Output Location: {'Default (model directory)' if use_default_location else str(output_dir)}\n\n")
        
        # Create and start worker thread
        self.worker = ConversionWorker(
            self.converter,
            self.model_path,
            str(output_path),
            precision,
            workspace_size,
            imgsz,
            batch,
            export_format,
            device,
            simplify,
            use_default_location
        )
        
        self.worker.progress.connect(self.on_conversion_progress)
        self.worker.progress_percent.connect(self.on_progress_percent_update)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.start()
    
    def on_conversion_progress(self, message: str):
        """Handle conversion progress updates."""
        self.progress_text.append(message)
        # Scroll to bottom
        self.progress_text.verticalScrollBar().setValue(
            self.progress_text.verticalScrollBar().maximum()
        )
    
    def on_progress_percent_update(self, percent: int):
        """Handle progress bar updates."""
        self.progress_bar.setValue(percent)
    
    def on_conversion_finished(self, success: bool, message: str):
        """Handle conversion completion."""
        self.convert_button.setEnabled(True)
        
        if success:
            self.statusBar().showMessage("Conversion completed successfully!")
            QMessageBox.information(self, "Success", message)
        else:
            self.statusBar().showMessage("Conversion failed!")
            QMessageBox.critical(self, "Error", message)
        
        self.worker = None


def run_gui():
    """Run the GUI application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
