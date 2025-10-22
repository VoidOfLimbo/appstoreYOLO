"""
Main GUI application for TensorRT Model Converter.
"""
import sys
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QGroupBox,
    QFileDialog, QSpinBox, QProgressBar, QMessageBox
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
    finished = pyqtSignal(bool, str)
    
    def __init__(
        self,
        converter: TensorRTConverter,
        model_path: str,
        engine_path: str,
        precision: str,
        workspace_size: int
    ):
        super().__init__()
        self.converter = converter
        self.model_path = model_path
        self.engine_path = engine_path
        self.precision = precision
        self.workspace_size = workspace_size
    
    def run(self):
        """Run the conversion in a separate thread."""
        try:
            model_ext = Path(self.model_path).suffix.lower()
            
            if model_ext == '.onnx':
                success = self.converter.convert_onnx_to_engine(
                    self.model_path,
                    self.engine_path,
                    self.precision,
                    self.workspace_size,
                    progress_callback=self.progress.emit
                )
            elif model_ext in ['.pt', '.pth']:
                # For PyTorch models, we need input shape
                # Using a default shape, but this should be configurable
                success = self.converter.convert_pytorch_to_engine(
                    self.model_path,
                    self.engine_path,
                    input_shape=(1, 3, 640, 640),  # Default YOLO shape
                    precision=self.precision,
                    workspace_size=self.workspace_size,
                    progress_callback=self.progress.emit
                )
            else:
                success = False
                message = f"Unsupported file format: {model_ext}"
                self.finished.emit(False, message)
                return
            
            if success:
                message = f"Conversion completed successfully!\nEngine saved to: {self.engine_path}"
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
        self.convert_button = QPushButton("Convert to TensorRT Engine")
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
        
        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.file_dropped.connect(self.on_file_dropped)
        layout.addWidget(self.drop_zone)
        
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
        
        # Workspace size setting
        workspace_layout = QHBoxLayout()
        workspace_layout.addWidget(QLabel("Workspace Size (GB):"))
        
        self.workspace_spin = QSpinBox()
        self.workspace_spin.setMinimum(1)
        self.workspace_spin.setMaximum(16)
        self.workspace_spin.setValue(DEFAULT_WORKSPACE_SIZE)
        workspace_layout.addWidget(self.workspace_spin)
        
        layout.addLayout(workspace_layout)
        
        # Output path
        output_label = QLabel("Output Directory:")
        layout.addWidget(output_label)
        
        output_path_layout = QHBoxLayout()
        
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setText(str(OUTPUT_DIR))
        output_path_layout.addWidget(self.output_path_edit)
        
        output_browse_button = QPushButton("Browse...")
        output_browse_button.clicked.connect(self.browse_output_dir)
        output_path_layout.addWidget(output_browse_button)
        
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
        output_dir = Path(self.output_path_edit.text())
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output engine path
        model_name = Path(self.model_path).stem
        engine_path = output_dir / f"{model_name}_{precision}.engine"
        
        # Disable UI during conversion
        self.convert_button.setEnabled(False)
        self.statusBar().showMessage("Converting...")
        self.progress_text.clear()
        self.progress_text.append("Starting conversion...\n")
        
        # Create and start worker thread
        self.worker = ConversionWorker(
            self.converter,
            self.model_path,
            str(engine_path),
            precision,
            workspace_size
        )
        
        self.worker.progress.connect(self.on_conversion_progress)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.start()
    
    def on_conversion_progress(self, message: str):
        """Handle conversion progress updates."""
        self.progress_text.append(message)
        # Scroll to bottom
        self.progress_text.verticalScrollBar().setValue(
            self.progress_text.verticalScrollBar().maximum()
        )
    
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
