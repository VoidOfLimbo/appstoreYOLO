"""Object Detection Application.

This sub-application provides object detection capabilities using OpenCV.
"""

import os
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from main_app.utils.base_app import BaseApp


class DetectionApp(BaseApp):
    """Object detection application using OpenCV."""
    
    def __init__(self, app_path: str):
        """Initialize the detection app.
        
        Args:
            app_path: Path to the app directory
        """
        super().__init__(app_path)
        self.current_image = None
        self.processed_image = None
    
    def initialize(self) -> bool:
        """Initialize the detection models and resources.
        
        Returns:
            True if successful
        """
        try:
            print(f"Initializing {self.name}...")
            # Initialize detection models here
            # For demo purposes, we'll use simple blob detection
            self.detector_params = cv2.SimpleBlobDetector_Params()
            self.detector_params.filterByArea = True
            self.detector_params.minArea = 100
            self.detector = cv2.SimpleBlobDetector_create(self.detector_params)
            print(f"{self.name} initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing {self.name}: {e}")
            return False
    
    def create_widget(self) -> QWidget:
        """Create the detection UI widget.
        
        Returns:
            QWidget for the detection app
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Description card
        desc_card = QWidget()
        desc_card.setStyleSheet("""
            background-color: #2D2D2D;
            border-radius: 12px;
        """)
        desc_layout = QVBoxLayout(desc_card)
        desc_layout.setContentsMargins(25, 20, 25, 20)
        
        desc = QLabel(self.description)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 11pt; color: #B0B0B0; line-height: 1.6;")
        desc_layout.addWidget(desc)
        
        layout.addWidget(desc_card)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        load_btn = QPushButton("📁 Load Image")
        load_btn.clicked.connect(self.load_image)
        load_btn.setCursor(Qt.PointingHandCursor)
        load_btn.setMinimumHeight(40)
        btn_layout.addWidget(load_btn)
        
        detect_btn = QPushButton("🔍 Detect Objects")
        detect_btn.clicked.connect(self.detect_objects)
        detect_btn.setCursor(Qt.PointingHandCursor)
        detect_btn.setMinimumHeight(40)
        detect_btn.setStyleSheet("background-color: #27AE60;")  # Success color
        btn_layout.addWidget(detect_btn)
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_display)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setMinimumHeight(40)
        clear_btn.setProperty("class", "secondary")
        btn_layout.addWidget(clear_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Image display in card
        image_card = QWidget()
        image_card.setStyleSheet("""
            background-color: #2D2D2D;
            border-radius: 12px;
            border: 2px solid #404040;
        """)
        image_layout = QVBoxLayout(image_card)
        image_layout.setContentsMargins(15, 15, 15, 15)
        
        self.image_label = QLabel("📷 No image loaded - Click 'Load Image' to begin")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 450)
        self.image_label.setStyleSheet("""
            color: #707070;
            font-size: 13pt;
            background-color: #1E1E1E;
            border-radius: 8px;
            padding: 30px;
        """)
        image_layout.addWidget(self.image_label)
        
        layout.addWidget(image_card)
        
        # Results display
        results_label = QLabel("📊 Detection Results")
        results_label.setStyleSheet("""
            font-size: 12pt;
            font-weight: bold;
            color: #3498DB;
            padding: 10px 0px;
        """)
        layout.addWidget(results_label)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(120)
        self.results_text.setStyleSheet("""
            background-color: #2D2D2D;
            border: 1px solid #404040;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Consolas', 'Courier New', monospace;
        """)
        layout.addWidget(self.results_text)
        
        return widget
    
    def load_image(self):
        """Load an image file."""
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.current_image = cv2.imread(file_path)
            if self.current_image is not None:
                self.display_image(self.current_image)
                self.results_text.setText(f"Loaded: {os.path.basename(file_path)}")
            else:
                self.results_text.setText("Error loading image")
    
    def detect_objects(self):
        """Perform object detection on the loaded image."""
        if self.current_image is None:
            self.results_text.setText("Please load an image first")
            return
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            
            # Detect blobs
            keypoints = self.detector.detect(gray)
            
            # Draw detections
            result_image = self.current_image.copy()
            result_image = cv2.drawKeypoints(
                result_image, keypoints, np.array([]), (0, 255, 0),
                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )
            
            self.processed_image = result_image
            self.display_image(result_image)
            
            # Display results
            self.results_text.setText(
                f"Detected {len(keypoints)} objects\n"
                f"Image size: {self.current_image.shape[1]}x{self.current_image.shape[0]}"
            )
            
        except Exception as e:
            self.results_text.setText(f"Error during detection: {e}")
    
    def display_image(self, image):
        """Display an OpenCV image in the label.
        
        Args:
            image: OpenCV image (BGR format)
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        
        # Convert to QImage
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Scale to fit label
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
    
    def clear_display(self):
        """Clear the display."""
        self.current_image = None
        self.processed_image = None
        self.image_label.setText("No image loaded")
        self.results_text.clear()
    
    def process(self, data):
        """Process input data (image).
        
        Args:
            data: Input image
            
        Returns:
            Processed image with detections
        """
        if data is None:
            return None
        
        try:
            gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
            keypoints = self.detector.detect(gray)
            result = cv2.drawKeypoints(
                data, keypoints, np.array([]), (0, 255, 0),
                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )
            return result
        except Exception as e:
            print(f"Error processing: {e}")
            return data
    
    def cleanup(self):
        """Clean up resources."""
        print(f"Cleaning up {self.name}...")
        self.current_image = None
        self.processed_image = None
