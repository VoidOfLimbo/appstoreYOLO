"""Custom card widget for displaying apps in a modern card-based layout."""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor


class AppCard(QFrame):
    """A modern card widget for displaying an application."""
    
    clicked = pyqtSignal(object)  # Emits the app_info dict when clicked
    
    def __init__(self, app_info, app_instance, parent=None):
        """Initialize the app card.
        
        Args:
            app_info: Dictionary with app information (name, version, description, icon)
            app_instance: The actual app instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.app_info = app_info
        self.app_instance = app_instance
        self.is_selected = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the card UI."""
        self.setFrameShape(QFrame.StyledPanel)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)
        
        # Apply default style
        self.apply_style(selected=False)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(15)
        
        # Icon on the left
        icon_label = QLabel(self.app_info.get('icon', '📦'))
        icon_label.setStyleSheet("font-size: 40px;")
        icon_label.setFixedSize(60, 60)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Text content in the middle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        # App name
        name_label = QLabel(self.app_info['name'])
        name_label.setStyleSheet("""
            font-size: 13pt;
            font-weight: bold;
            color: #E8E8E8;
        """)
        text_layout.addWidget(name_label)
        
        # App version
        version_label = QLabel(f"v{self.app_info['version']}")
        version_label.setStyleSheet("""
            font-size: 9pt;
            color: #888888;
        """)
        text_layout.addWidget(version_label)
        
        # App description
        desc_label = QLabel(self.app_info['description'])
        desc_label.setStyleSheet("""
            font-size: 9pt;
            color: #AAAAAA;
        """)
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout, 1)
        
        # Arrow indicator on the right
        arrow_label = QLabel("›")
        arrow_label.setStyleSheet("""
            font-size: 32pt;
            color: #555555;
            font-weight: bold;
        """)
        arrow_label.setFixedWidth(30)
        arrow_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(arrow_label)
        
    def apply_style(self, selected=False):
        """Apply styling to the card based on selection state.
        
        Args:
            selected: Whether the card is selected
        """
        self.is_selected = selected
        
        if selected:
            # Selected state - accent color
            self.setStyleSheet("""
                AppCard {
                    background-color: #2A4B7C;
                    border: 2px solid #4A9EFF;
                    border-radius: 10px;
                }
                AppCard:hover {
                    background-color: #2E5189;
                    border: 2px solid #5AADFF;
                }
            """)
        else:
            # Default state
            self.setStyleSheet("""
                AppCard {
                    background-color: #2D2D2D;
                    border: 1px solid #404040;
                    border-radius: 10px;
                }
                AppCard:hover {
                    background-color: #353535;
                    border: 1px solid #4A9EFF;
                }
            """)
    
    def mousePressEvent(self, event):
        """Handle mouse press event.
        
        Args:
            event: Mouse event
        """
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.app_info)
        super().mousePressEvent(event)
    
    def set_selected(self, selected):
        """Set the selection state of the card.
        
        Args:
            selected: Whether the card should be selected
        """
        self.apply_style(selected=selected)
