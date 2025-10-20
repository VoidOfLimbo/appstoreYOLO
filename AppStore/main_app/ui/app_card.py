"""Custom card widget for displaying apps in a modern card-based layout."""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor
from main_app.ui.theme import ModernTheme


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
        self.setFrameShape(QFrame.NoFrame)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(90)
        # Remove maximum height to allow card to scale with content
        
        # Apply default style (no background initially)
        self.apply_style(selected=False)
        
        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Icon on the left
        icon_label = QLabel(self.app_info.get('icon', '📦'))
        icon_label.setStyleSheet("font-size: 36px; background-color: transparent;")
        icon_label.setFixedSize(48, 48)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Text content in the middle
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        # App name
        name_label = QLabel(self.app_info['name'])
        name_label.setStyleSheet(f"""
            font-size: 13pt;
            font-weight: 600;
            color: {ModernTheme.TEXT_PRIMARY};
            background-color: transparent;
        """)
        text_layout.addWidget(name_label)
        
        # App version
        version_label = QLabel(f"v{self.app_info['version']}")
        version_label.setStyleSheet(f"""
            font-size: 9pt;
            color: {ModernTheme.TEXT_MUTED};
            background-color: transparent;
        """)
        text_layout.addWidget(version_label)
        
        # App description
        desc_label = QLabel(self.app_info['description'])
        desc_label.setStyleSheet(f"""
            font-size: 9pt;
            color: {ModernTheme.TEXT_SECONDARY};
            background-color: transparent;
        """)
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout, 1)
        
        # Arrow indicator on the right
        arrow_label = QLabel("›")
        arrow_label.setStyleSheet(f"""
            font-size: 28pt;
            color: {ModernTheme.TEXT_MUTED};
            font-weight: 300;
            background-color: transparent;
        """)
        arrow_label.setFixedWidth(24)
        arrow_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(arrow_label)
        
    def apply_style(self, selected=False):
        """Apply styling to the card based on selection state.
        
        Args:
            selected: Whether the card is selected
        """
        self.is_selected = selected
        
        if selected:
            # Selected state - subtle border and accent
            self.setStyleSheet(f"""
                AppCard {{
                    background-color: transparent;
                    border: 2px solid {ModernTheme.ACCENT};
                    border-radius: 4px;
                }}
            """)
        else:
            # Default state - subtle border on hover only
            self.setStyleSheet(f"""
                AppCard {{
                    background-color: transparent;
                    border: 1px solid transparent;
                    border-radius: 4px;
                }}
                AppCard:hover {{
                    border: 1px solid {ModernTheme.BORDER_LIGHT};
                    background-color: {ModernTheme.BG_HOVER};
                }}
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
