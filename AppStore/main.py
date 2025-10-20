"""Main entry point for the AppStore application.

This module creates the main UI dashboard and handles the application lifecycle.
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QListWidget, QStackedWidget,
                             QLabel, QStatusBar, QMessageBox, QSplitter, QFrame, 
                             QScrollArea)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QFont

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from main_app.utils.app_loader import AppLoader
from main_app.ui.theme import ModernTheme
from main_app.ui.app_card import AppCard


class MainWindow(QMainWindow):
    """Main application window with dashboard UI."""
    
    def __init__(self):
        super().__init__()
        self.app_loader = None
        self.loaded_apps = {}
        self.app_cards = []  # Store card widgets
        self.selected_card = None  # Track selected card
        self.init_ui()
        self.load_apps()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("AppStore - Modular AI Application Platform")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1000, 700)
        
        # Apply modern theme
        self.setStyleSheet(ModernTheme.get_stylesheet())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with no margins
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(1)
        
        # Left panel - App list
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - App display area
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes (25% left, 75% right)
        splitter.setSizes([350, 1050])
        
        main_layout.addWidget(splitter)
        
        # Status bar with modern style
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🚀 Ready - All systems operational")
    
    def create_left_panel(self) -> QWidget:
        """Create the left panel with app list.
        
        Returns:
            Widget containing the app list
        """
        panel = QWidget()
        panel.setStyleSheet(ModernTheme.get_panel_style())
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 12, 8, 12)
        layout.setSpacing(8)
        
        # Logo/Title section
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        app_title = QLabel("🚀 AppStore")
        app_title.setProperty("class", "title")
        app_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(app_title)
        
        subtitle = QLabel("AI Application Platform")
        subtitle.setProperty("class", "subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        layout.addWidget(title_container)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"background-color: {ModernTheme.BORDER};")
        layout.addWidget(line)
        
        # Apps section label
        apps_label = QLabel("📱 INSTALLED APPS")
        apps_label.setProperty("class", "header")
        layout.addWidget(apps_label)
        
        # Scroll area for app cards
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2D2D2D;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666666;
            }
        """)
        
        # Container widget for cards
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(4)
        self.cards_layout.addStretch()  # Push cards to top
        
        scroll_area.setWidget(self.cards_container)
        layout.addWidget(scroll_area)
        
        # Button container
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(4)
        
        # Refresh button with icon
        refresh_btn = QPushButton("🔄 Refresh Apps")
        refresh_btn.clicked.connect(self.refresh_apps)
        refresh_btn.setProperty("class", "secondary")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(refresh_btn)
        
        # About button with icon
        about_btn = QPushButton("ℹ️ About")
        about_btn.clicked.connect(self.show_about)
        about_btn.setProperty("class", "secondary")
        about_btn.setCursor(Qt.PointingHandCursor)
        button_layout.addWidget(about_btn)
        
        layout.addWidget(button_container)
        
        return panel
    
    def create_right_panel(self) -> QWidget:
        """Create the right panel for displaying app content.
        
        Returns:
            Widget containing the stacked widget for apps
        """
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Top bar with app info
        top_bar = QWidget()
        top_bar.setStyleSheet(ModernTheme.get_card_style())
        top_bar.setMinimumHeight(56)
        top_bar.setMaximumHeight(56)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(12, 8, 12, 8)
        
        self.app_info_label = QLabel("Select an application from the list")
        self.app_info_label.setStyleSheet(f"""
            font-size: 13pt;
            font-weight: bold;
            color: {ModernTheme.TEXT_PRIMARY};
        """)
        top_bar_layout.addWidget(self.app_info_label)
        top_bar_layout.addStretch()
        
        layout.addWidget(top_bar)
        
        # Stacked widget for app UIs with card style
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget, 1)
        
        # Welcome screen
        welcome = self.create_welcome_screen()
        self.stacked_widget.addWidget(welcome)
        
        return panel
    
    def create_welcome_screen(self) -> QWidget:
        """Create the welcome screen.
        
        Returns:
            Welcome screen widget
        """
        widget = QWidget()
        widget.setStyleSheet(ModernTheme.get_card_style())
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        
        # Large icon/emoji
        icon_label = QLabel("🚀")
        icon_label.setStyleSheet("font-size: 96px; background-color: transparent;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title with modern font
        title = QLabel("Welcome to AppStore")
        title.setStyleSheet(f"""
            font-size: 32pt;
            font-weight: bold;
            color: {ModernTheme.ACCENT};
            background-color: transparent;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Your Modular AI Application Platform")
        subtitle.setStyleSheet(f"""
            font-size: 14pt;
            color: {ModernTheme.TEXT_SECONDARY};
            background-color: transparent;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Feature list in a card
        features_card = QWidget()
        features_card.setStyleSheet(f"""
            background-color: {ModernTheme.BG_LIGHT};
            border-radius: 4px;
            padding: 16px;
        """)
        features_card.setMaximumWidth(500)
        features_layout = QVBoxLayout(features_card)
        
        features = [
            ("🎯", "Object Detection", "Real-time object detection with OpenCV"),
            ("📍", "Object Tracking", "Multi-algorithm tracking system"),
            ("🏷️", "Classification", "Image classification with ML models"),
            ("⚡", "TensorRT", "GPU-accelerated model optimization"),
        ]
        
        for emoji, title_text, desc in features:
            feature_row = QWidget()
            feature_layout = QHBoxLayout(feature_row)
            feature_layout.setContentsMargins(4, 8, 4, 8)
            feature_layout.setSpacing(12)
            
            emoji_label = QLabel(emoji)
            emoji_label.setStyleSheet("font-size: 24pt; background-color: transparent;")
            emoji_label.setFixedWidth(48)
            emoji_label.setAlignment(Qt.AlignCenter)
            feature_layout.addWidget(emoji_label)
            
            text_layout = QVBoxLayout()
            text_layout.setSpacing(4)
            
            title_label = QLabel(title_text)
            title_label.setStyleSheet(f"""
                font-size: 12pt;
                font-weight: 600;
                color: {ModernTheme.TEXT_PRIMARY};
                background-color: transparent;
            """)
            text_layout.addWidget(title_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"""
                font-size: 10pt;
                color: {ModernTheme.TEXT_SECONDARY};
                background-color: transparent;
            """)
            desc_label.setWordWrap(True)
            text_layout.addWidget(desc_label)
            
            feature_layout.addLayout(text_layout)
            features_layout.addWidget(feature_row)
        
        layout.addWidget(features_card, 0, Qt.AlignCenter)
        
        # Get started hint
        hint = QLabel("👈 Select an app from the sidebar to begin")
        hint.setStyleSheet(f"""
            font-size: 11pt;
            color: {ModernTheme.TEXT_SECONDARY};
            padding: 12px;
            background-color: transparent;
        """)
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)
        
        return widget
    
    def load_apps(self):
        """Load all available applications."""
        try:
            apps_dir = os.path.join(project_root, "apps")
            self.app_loader = AppLoader(apps_dir)
            self.loaded_apps = self.app_loader.load_all_apps()
            
            # Add apps as cards
            for app_name, app_instance in self.loaded_apps.items():
                if app_instance.is_enabled():
                    info = app_instance.get_info()
                    
                    # Create card widget
                    card = AppCard(info, app_instance, self)
                    card.clicked.connect(self.on_card_clicked)
                    self.app_cards.append(card)
                    
                    # Insert before the stretch
                    self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)
                    
                    # Add app widget to stacked widget
                    try:
                        app_widget = app_instance.get_widget()
                        self.stacked_widget.addWidget(app_widget)
                    except Exception as e:
                        print(f"Error creating widget for {app_name}: {e}")
            
            self.status_bar.showMessage(f"Loaded {len(self.loaded_apps)} applications")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load applications: {e}")
            print(f"Error loading apps: {e}")
            import traceback
            traceback.print_exc()
    
    def refresh_apps(self):
        """Refresh the application list."""
        # Clear current card widgets
        for card in self.app_cards:
            self.cards_layout.removeWidget(card)
            card.deleteLater()
        self.app_cards.clear()
        self.selected_card = None
        
        # Clear stacked widget (except welcome screen)
        while self.stacked_widget.count() > 1:
            widget = self.stacked_widget.widget(1)
            self.stacked_widget.removeWidget(widget)
            widget.deleteLater()
        
        # Unload all apps
        if self.app_loader:
            self.app_loader.unload_all_apps()
        
        # Reload apps
        self.load_apps()
        self.stacked_widget.setCurrentIndex(0)
        self.app_info_label.setText("Select an application from the list")
        self.status_bar.showMessage("Applications refreshed")
    
    def on_card_clicked(self, app_info):
        """Handle card click event.
        
        Args:
            app_info: Dictionary with app information
        """
        # Deselect previous card
        if self.selected_card:
            self.selected_card.set_selected(False)
        
        # Find and select the clicked card
        for card in self.app_cards:
            if card.app_info == app_info:
                card.set_selected(True)
                self.selected_card = card
                break
        
        # Update info label
        self.app_info_label.setText(
            f"<b>{app_info['name']}</b> - {app_info['description']}"
        )
        
        # Find the corresponding app instance and switch to its widget
        for app_name, app_instance in self.loaded_apps.items():
            info = app_instance.get_info()
            if info['name'] == app_info['name']:
                app_widget = app_instance.get_widget()
                index = self.stacked_widget.indexOf(app_widget)
                if index != -1:
                    self.stacked_widget.setCurrentIndex(index)
                
                self.status_bar.showMessage(f"Loaded: {info['name']}")
                break
    
    def show_about(self):
        """Show about dialog."""
        about_text = f"""
        <div style='text-align: center;'>
            <h1 style='color: {ModernTheme.ACCENT}; margin-bottom: 8px;'>🚀 AppStore</h1>
            <h3 style='color: {ModernTheme.TEXT_SECONDARY}; margin-top: 0;'>
                Modular AI Application Platform
            </h3>
        </div>
        
        <p style='font-size: 11pt; margin-top: 16px;'>
            <b style='color: {ModernTheme.ACCENT};'>Version:</b> 1.0.0<br>
            <b style='color: {ModernTheme.ACCENT};'>CUDA Support:</b> 13.0 ✓<br>
            <b style='color: {ModernTheme.ACCENT};'>TensorRT:</b> 10.13.3.9 ✓
        </p>
        
        <p style='margin-top: 12px; color: {ModernTheme.TEXT_PRIMARY};'>
            A professional-grade modular application framework for AI and 
            computer vision applications with GPU acceleration.
        </p>
        
        <p style='margin-top: 12px; color: {ModernTheme.TEXT_PRIMARY};'><b style='color: {ModernTheme.ACCENT};'>✨ Key Features:</b></p>
        <ul style='margin-left: 16px; color: {ModernTheme.TEXT_PRIMARY};'>
            <li>🔌 Dynamic application loading system</li>
            <li>⚡ CUDA 13.0 & TensorRT acceleration</li>
            <li>🎨 Modern dark theme UI</li>
            <li>🔄 Hot-pluggable sub-applications</li>
            <li>📦 Easy deployment & updates</li>
            <li>🛠️ Extensible architecture</li>
        </ul>
        
        <p style='margin-top: 12px; color: {ModernTheme.TEXT_PRIMARY};'><b style='color: {ModernTheme.ACCENT};'>🔧 Technologies:</b></p>
        <p style='margin-left: 16px; color: {ModernTheme.TEXT_PRIMARY};'>
            PyQt5 • OpenCV • CuPy • TensorRT • NumPy • Python 3.10
        </p>
        
        <p style='margin-top: 16px; text-align: center; color: {ModernTheme.TEXT_SECONDARY};'>
            <small>© 2025 AppStore Team. All rights reserved.</small>
        </p>
        """
        
        # Create custom message box with modern styling
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("About AppStore")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(about_text)
        msg_box.setStyleSheet(ModernTheme.get_stylesheet())
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()
    
    def closeEvent(self, event):
        """Handle window close event.
        
        Args:
            event: Close event
        """
        # Clean up all apps
        if self.app_loader:
            self.app_loader.unload_all_apps()
        event.accept()


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("AppStore")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AppStore Team")
    
    # Set Fusion style as base (then override with stylesheet)
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
