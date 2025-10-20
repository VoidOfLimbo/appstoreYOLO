"""Object Tracking Application.

This sub-application provides object tracking capabilities using OpenCV trackers and StrongSORT.
"""

import os
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QTextEdit, QGroupBox, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from main_app.utils.base_app import BaseApp

# Check for StrongSORT availability
try:
    from boxmot import StrongSORT
    from ultralytics import YOLO
    STRONGSORT_AVAILABLE = True
except (ImportError, OSError) as e:
    # OSError handles DLL loading issues on Windows
    STRONGSORT_AVAILABLE = False
    print(f"StrongSORT not available: {type(e).__name__}")


class TrackingApp(BaseApp):
    """Object tracking application using OpenCV trackers and StrongSORT."""
    
    def __init__(self, app_path: str):
        """Initialize the tracking app.
        
        Args:
            app_path: Path to the app directory
        """
        super().__init__(app_path)
        self.tracker = None
        self.tracker_types = [
            'BOOSTING', 'MIL', 'KCF', 'TLD', 
            'MEDIANFLOW', 'MOSSE', 'CSRT', 'StrongSORT'
        ]
        self.models_dir = Path(project_root) / 'models'
    
    def initialize(self) -> bool:
        """Initialize the tracking resources.
        
        Returns:
            True if successful
        """
        try:
            print(f"Initializing {self.name}...")
            # Trackers are initialized on-demand
            print(f"{self.name} initialized successfully")
            return True
        except Exception as e:
            print(f"Error initializing {self.name}: {e}")
            return False
    
    def create_widget(self) -> QWidget:
        """Create the tracking UI widget.
        
        Returns:
            QWidget for the tracking app
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🎯 Object Tracking")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Track objects in videos using multiple algorithms including OpenCV trackers "
            "and advanced StrongSORT with Re-ID features."
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("font-size: 14px; color: #7f8c8d; line-height: 1.6; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Tracker Configuration Group
        config_group = QGroupBox("⚙️ Tracker Configuration")
        config_layout = QVBoxLayout()
        config_layout.setContentsMargins(20, 20, 20, 20)
        config_layout.setSpacing(15)
        
        # Tracker selection
        tracker_layout = QHBoxLayout()
        tracker_label = QLabel("Tracker Algorithm:")
        tracker_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        tracker_layout.addWidget(tracker_label)
        
        self.tracker_combo = QComboBox()
        self.tracker_combo.addItems(self.tracker_types)
        self.tracker_combo.setCurrentText('CSRT')
        self.tracker_combo.currentTextChanged.connect(self._on_tracker_changed)
        self.tracker_combo.setMinimumHeight(35)
        self.tracker_combo.setStyleSheet("""
            QComboBox {
                padding: 5px 10px;
                font-size: 13px;
                background-color: #34495E;
                border: 2px solid #3498DB;
                border-radius: 5px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        tracker_layout.addWidget(self.tracker_combo)
        tracker_layout.addStretch()
        config_layout.addLayout(tracker_layout)
        
        # Tracker info display
        self.tracker_info = QLabel()
        self.tracker_info.setWordWrap(True)
        self.tracker_info.setStyleSheet("""
            QLabel {
                padding: 15px;
                background-color: #34495E;
                border-radius: 8px;
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        self._update_tracker_info('CSRT')
        config_layout.addWidget(self.tracker_info)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Features Group
        features_group = QGroupBox("✨ Features")
        features_layout = QVBoxLayout()
        features_layout.setContentsMargins(20, 20, 20, 20)
        features_layout.setSpacing(12)
        
        features = [
            ("🎯", "Multiple Algorithms", "Choose from 7 OpenCV trackers + StrongSORT"),
            ("⚡", "Real-time Performance", "Optimized for fast tracking with GPU support"),
            ("🛡️", "Robust Tracking", "Handle occlusions and appearance changes"),
            ("🧠", "Re-ID Features", "StrongSORT uses deep learning for re-identification"),
        ]
        
        for emoji, title_text, desc_text in features:
            feature_layout = QHBoxLayout()
            feature_layout.setSpacing(12)
            
            emoji_label = QLabel(emoji)
            emoji_label.setStyleSheet("font-size: 24px;")
            emoji_label.setFixedWidth(40)
            feature_layout.addWidget(emoji_label)
            
            text_layout = QVBoxLayout()
            text_layout.setSpacing(2)
            
            title_label = QLabel(title_text)
            title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
            text_layout.addWidget(title_label)
            
            desc_label = QLabel(desc_text)
            desc_label.setStyleSheet("font-size: 11px; color: #95A5A6;")
            desc_label.setWordWrap(True)
            text_layout.addWidget(desc_label)
            
            feature_layout.addLayout(text_layout)
            features_layout.addLayout(feature_layout)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        # Status Group
        status_group = QGroupBox("📊 Status")
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(15, 15, 15, 15)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 2px solid #34495E;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                color: #ECF0F1;
            }
        """)
        
        status_msg = "Tracking app ready.\n\n"
        if STRONGSORT_AVAILABLE:
            status_msg += "✓ StrongSORT is available\n"
            status_msg += "✓ YOLO detection is available\n"
        else:
            status_msg += "⚠️ StrongSORT not available (install boxmot)\n"
        status_msg += f"✓ {len(self.tracker_types)-1} OpenCV trackers available\n"
        
        self.status_text.setText(status_msg)
        status_layout.addWidget(self.status_text)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Add stretch to push content to top
        layout.addStretch()
        
        return widget
    
    def _on_tracker_changed(self, tracker_name):
        """Handle tracker selection change."""
        self._update_tracker_info(tracker_name)
    
    def _update_tracker_info(self, tracker_name):
        """Update tracker information display."""
        tracker_info = {
            'BOOSTING': {
                'name': 'Boosting Tracker',
                'speed': 'Slow',
                'accuracy': 'Moderate',
                'desc': 'Based on AdaBoost algorithm. Good for simple scenarios but slower than others.'
            },
            'MIL': {
                'name': 'Multiple Instance Learning',
                'speed': 'Moderate',
                'accuracy': 'Good',
                'desc': 'Robust to partial occlusions. Better than BOOSTING in most cases.'
            },
            'KCF': {
                'name': 'Kernelized Correlation Filters',
                'speed': 'Fast',
                'accuracy': 'Good',
                'desc': 'Fast and accurate for most scenarios. Good balance of speed and performance.'
            },
            'TLD': {
                'name': 'Tracking, Learning and Detection',
                'speed': 'Slow',
                'accuracy': 'Good',
                'desc': 'Can recover from occlusions and track lost objects. Slower but robust.'
            },
            'MEDIANFLOW': {
                'name': 'Median Flow',
                'speed': 'Fast',
                'accuracy': 'Moderate',
                'desc': 'Fast and reliable for predictable motion. Fails on fast movements.'
            },
            'MOSSE': {
                'name': 'Minimum Output Sum of Squared Error',
                'speed': 'Very Fast',
                'accuracy': 'Moderate',
                'desc': 'Extremely fast but less accurate. Good for real-time applications.'
            },
            'CSRT': {
                'name': 'Discriminative Correlation Filter with Channel and Spatial Reliability',
                'speed': 'Moderate',
                'accuracy': 'Excellent',
                'desc': 'Most accurate OpenCV tracker. Best for complex scenarios and occlusions.'
            },
            'StrongSORT': {
                'name': 'StrongSORT with Re-ID',
                'speed': 'Moderate',
                'accuracy': 'Excellent',
                'desc': 'State-of-the-art multi-object tracking with deep learning Re-ID. '
                        'Best for crowded scenes and long-term tracking. Requires YOLO detection model.'
            }
        }
        
        info = tracker_info.get(tracker_name, {})
        
        info_html = f"""
        <b style='font-size: 14px;'>{info.get('name', tracker_name)}</b><br><br>
        <b>Speed:</b> <span style='color: #3498DB;'>{info.get('speed', 'N/A')}</span><br>
        <b>Accuracy:</b> <span style='color: #27AE60;'>{info.get('accuracy', 'N/A')}</span><br><br>
        {info.get('desc', 'No description available.')}
        """
        
        if tracker_name == 'StrongSORT' and not STRONGSORT_AVAILABLE:
            info_html += "<br><br><span style='color: #E74C3C;'>⚠️ StrongSORT requires 'boxmot' package. Install with: pip install boxmot</span>"
        
        self.tracker_info.setText(info_html)
    
    def create_tracker(self, tracker_type: str):
        """Create a tracker of the specified type.
        
        Args:
            tracker_type: Type of tracker to create
            
        Returns:
            Tracker object (OpenCV or StrongSORT)
        """
        tracker_type = tracker_type.upper()
        
        if tracker_type == 'STRONGSORT':
            if not STRONGSORT_AVAILABLE:
                raise ImportError("StrongSORT requires 'boxmot' package. Install with: pip install boxmot")
            
            # Path to StrongSORT Re-ID model
            reid_model = self.models_dir / 'tracking' / 'strongsort' / 'osnet_x0_25_msmt17.pt'
            
            if not reid_model.exists():
                raise FileNotFoundError(
                    f"StrongSORT Re-ID model not found at: {reid_model}\n"
                    "Run download_models.py to download the model."
                )
            
            # Create StrongSORT tracker
            tracker = StrongSORT(
                model_weights=reid_model,
                device='cuda:0' if cv2.cuda.getCudaEnabledDeviceCount() > 0 else 'cpu',
                fp16=True,
                max_dist=0.2,
                max_iou_distance=0.7,
                max_age=30,
                n_init=3,
                nn_budget=100,
            )
            return tracker
        
        # OpenCV trackers
        if tracker_type == 'BOOSTING':
            return cv2.legacy.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            return cv2.legacy.TrackerMIL_create()
        elif tracker_type == 'KCF':
            return cv2.legacy.TrackerKCF_create()
        elif tracker_type == 'TLD':
            return cv2.legacy.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            return cv2.legacy.TrackerMedianFlow_create()
        elif tracker_type == 'MOSSE':
            return cv2.legacy.TrackerMOSSE_create()
        elif tracker_type == 'CSRT':
            return cv2.legacy.TrackerCSRT_create()
        else:
            return cv2.legacy.TrackerCSRT_create()
    
    def process(self, data):
        """Process input data for tracking.
        
        Args:
            data: Input frame
            
        Returns:
            Processed frame with tracking visualization
        """
        # This is a placeholder - actual tracking would require
        # video feed and ROI selection
        return data
    
    def cleanup(self):
        """Clean up resources."""
        print(f"Cleaning up {self.name}...")
        self.tracker = None
