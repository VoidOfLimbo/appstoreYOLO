"""Image Classification Application.

This sub-application provides image classification capabilities.
"""

import os
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QTextEdit, QProgressBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from main_app.utils.base_app import BaseApp


class ClassificationApp(BaseApp):
    """Image classification application."""
    
    def __init__(self, app_path: str):
        """Initialize the classification app.
        
        Args:
            app_path: Path to the app directory
        """
        super().__init__(app_path)
        self.current_image = None
        self.model_loaded = False
    
    def initialize(self) -> bool:
        """Initialize the classification models.
        
        Returns:
            True if successful
        """
        try:
            print(f"Initializing {self.name}...")
            # In a real application, you would load a pre-trained model here
            # For demo purposes, we'll simulate classification
            self.classes = [
                'cat', 'dog', 'bird', 'car', 'bicycle', 
                'person', 'airplane', 'boat', 'tree', 'flower'
            ]
            self.model_loaded = True
            print(f"{self.name} initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing {self.name}: {e}")
            return False
    
    def create_widget(self) -> QWidget:
        """Create the classification UI widget.
        
        Returns:
            QWidget for the classification app
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
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load Image")
        load_btn.clicked.connect(self.load_image)
        btn_layout.addWidget(load_btn)
        
        classify_btn = QPushButton("Classify")
        classify_btn.clicked.connect(self.classify_image)
        btn_layout.addWidget(classify_btn)
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_display)
        btn_layout.addWidget(clear_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Image display
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600, 400)
        self.image_label.setStyleSheet("border: 2px solid gray; background-color: #f0f0f0;")
        layout.addWidget(self.image_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setMaximumHeight(150)
        layout.addWidget(QLabel("Classification Results:"))
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
    
    def classify_image(self):
        """Classify the loaded image."""
        if self.current_image is None:
            self.results_text.setText("Please load an image first")
            return
        
        if not self.model_loaded:
            self.results_text.setText("Model not loaded")
            return
        
        try:
            # Show progress
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(30)
            
            # Simulate classification (in real app, use actual model)
            # For demo, we'll generate random predictions
            predictions = []
            np.random.seed(sum(self.current_image.flatten().astype(int)) % 1000)
            
            for i, class_name in enumerate(self.classes):
                confidence = np.random.random()
                predictions.append((class_name, confidence))
            
            self.progress_bar.setValue(70)
            
            # Sort by confidence
            predictions.sort(key=lambda x: x[1], reverse=True)
            
            self.progress_bar.setValue(100)
            
            # Display top 5 predictions
            result_text = "Top 5 Predictions:\n\n"
            for i, (class_name, confidence) in enumerate(predictions[:5], 1):
                result_text += f"{i}. {class_name}: {confidence*100:.2f}%\n"
            
            result_text += f"\nImage size: {self.current_image.shape[1]}x{self.current_image.shape[0]}"
            
            self.results_text.setText(result_text)
            self.progress_bar.setVisible(False)
            
        except Exception as e:
            self.results_text.setText(f"Error during classification: {e}")
            self.progress_bar.setVisible(False)
    
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
        self.image_label.setText("No image loaded")
        self.results_text.clear()
        self.progress_bar.setVisible(False)
    
    def process(self, data):
        """Process input data (image) for classification.
        
        Args:
            data: Input image
            
        Returns:
            Classification results
        """
        if data is None or not self.model_loaded:
            return None
        
        # Simulate classification
        predictions = []
        for class_name in self.classes[:3]:
            confidence = np.random.random()
            predictions.append((class_name, confidence))
        
        return predictions
    
    def cleanup(self):
        """Clean up resources."""
        print(f"Cleaning up {self.name}...")
        self.current_image = None
        self.model_loaded = False
