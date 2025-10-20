"""Modern UI Theme Configuration.

This module provides a modern dark theme with consistent styling across the application.
"""

class ModernTheme:
    """Modern dark theme with accent colors."""
    
    # Main colors
    PRIMARY = "#2C3E50"        # Dark blue-gray
    SECONDARY = "#34495E"      # Lighter blue-gray
    ACCENT = "#3498DB"         # Bright blue
    ACCENT_HOVER = "#5DADE2"   # Light blue
    SUCCESS = "#27AE60"        # Green
    WARNING = "#F39C12"        # Orange
    DANGER = "#E74C3C"         # Red
    INFO = "#9B59B6"           # Purple
    
    # Background colors
    BG_DARK = "#1E1E1E"        # Very dark gray
    BG_MEDIUM = "#252525"      # Dark gray
    BG_LIGHT = "#2D2D2D"       # Medium gray
    BG_HOVER = "#3A3A3A"       # Light gray for hover
    
    # Text colors
    TEXT_PRIMARY = "#FFFFFF"   # White
    TEXT_SECONDARY = "#B0B0B0" # Light gray
    TEXT_DISABLED = "#707070"  # Medium gray
    
    # Border colors
    BORDER = "#404040"         # Dark border
    BORDER_LIGHT = "#505050"   # Light border
    
    @staticmethod
    def get_stylesheet():
        """Get the complete stylesheet for the application."""
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {ModernTheme.BG_DARK};
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        /* Central Widget */
        QWidget {{
            background-color: {ModernTheme.BG_DARK};
            color: {ModernTheme.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {ModernTheme.ACCENT};
            color: {ModernTheme.TEXT_PRIMARY};
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            min-height: 35px;
        }}
        
        QPushButton:hover {{
            background-color: {ModernTheme.ACCENT_HOVER};
        }}
        
        QPushButton:pressed {{
            background-color: {ModernTheme.PRIMARY};
        }}
        
        QPushButton:disabled {{
            background-color: {ModernTheme.BG_LIGHT};
            color: {ModernTheme.TEXT_DISABLED};
        }}
        
        /* Secondary Buttons */
        QPushButton[class="secondary"] {{
            background-color: {ModernTheme.SECONDARY};
        }}
        
        QPushButton[class="secondary"]:hover {{
            background-color: {ModernTheme.BG_HOVER};
        }}
        
        /* Success Button */
        QPushButton[class="success"] {{
            background-color: {ModernTheme.SUCCESS};
        }}
        
        /* Warning Button */
        QPushButton[class="warning"] {{
            background-color: {ModernTheme.WARNING};
        }}
        
        /* Danger Button */
        QPushButton[class="danger"] {{
            background-color: {ModernTheme.DANGER};
        }}
        
        /* List Widget */
        QListWidget {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 8px;
            padding: 8px;
            outline: none;
        }}
        
        QListWidget::item {{
            background-color: {ModernTheme.BG_LIGHT};
            border: none;
            border-radius: 6px;
            padding: 12px;
            margin: 4px 0px;
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        QListWidget::item:hover {{
            background-color: {ModernTheme.BG_HOVER};
        }}
        
        QListWidget::item:selected {{
            background-color: {ModernTheme.ACCENT};
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        /* Labels */
        QLabel {{
            color: {ModernTheme.TEXT_PRIMARY};
            background-color: transparent;
        }}
        
        QLabel[class="title"] {{
            font-size: 24pt;
            font-weight: bold;
            color: {ModernTheme.ACCENT};
        }}
        
        QLabel[class="subtitle"] {{
            font-size: 14pt;
            color: {ModernTheme.TEXT_SECONDARY};
        }}
        
        QLabel[class="header"] {{
            font-size: 12pt;
            font-weight: bold;
            color: {ModernTheme.ACCENT};
            padding: 8px;
        }}
        
        /* Text Edit */
        QTextEdit {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 6px;
            padding: 10px;
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        /* Line Edit */
        QLineEdit {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 6px;
            padding: 8px;
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        QLineEdit:focus {{
            border: 1px solid {ModernTheme.ACCENT};
        }}
        
        /* Combo Box */
        QComboBox {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 6px;
            padding: 8px;
            color: {ModernTheme.TEXT_PRIMARY};
            min-height: 30px;
        }}
        
        QComboBox:hover {{
            border: 1px solid {ModernTheme.ACCENT};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: url(down_arrow.png);
            width: 12px;
            height: 12px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            selection-background-color: {ModernTheme.ACCENT};
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        /* Spin Box */
        QSpinBox {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 6px;
            padding: 8px;
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        QSpinBox:focus {{
            border: 1px solid {ModernTheme.ACCENT};
        }}
        
        /* Check Box */
        QCheckBox {{
            color: {ModernTheme.TEXT_PRIMARY};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid {ModernTheme.BORDER};
            background-color: {ModernTheme.BG_MEDIUM};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {ModernTheme.ACCENT};
            border: 2px solid {ModernTheme.ACCENT};
        }}
        
        /* Group Box */
        QGroupBox {{
            border: 2px solid {ModernTheme.BORDER};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 16px;
            font-weight: bold;
            color: {ModernTheme.ACCENT};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px 0 8px;
            background-color: {ModernTheme.BG_DARK};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 6px;
            text-align: center;
            color: {ModernTheme.TEXT_PRIMARY};
            height: 25px;
        }}
        
        QProgressBar::chunk {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {ModernTheme.ACCENT},
                stop:1 {ModernTheme.ACCENT_HOVER}
            );
            border-radius: 6px;
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {ModernTheme.BG_MEDIUM};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {ModernTheme.BORDER_LIGHT};
            border-radius: 6px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {ModernTheme.ACCENT};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {ModernTheme.BG_MEDIUM};
            height: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {ModernTheme.BORDER_LIGHT};
            border-radius: 6px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {ModernTheme.ACCENT};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        /* Splitter */
        QSplitter::handle {{
            background-color: {ModernTheme.BORDER};
        }}
        
        QSplitter::handle:hover {{
            background-color: {ModernTheme.ACCENT};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {ModernTheme.BG_MEDIUM};
            color: {ModernTheme.TEXT_SECONDARY};
            border-top: 1px solid {ModernTheme.BORDER};
        }}
        
        /* Tool Tip */
        QToolTip {{
            background-color: {ModernTheme.BG_LIGHT};
            color: {ModernTheme.TEXT_PRIMARY};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 4px;
            padding: 8px;
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {ModernTheme.BG_MEDIUM};
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        QMenuBar::item:selected {{
            background-color: {ModernTheme.ACCENT};
        }}
        
        /* Menu */
        QMenu {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        QMenu::item:selected {{
            background-color: {ModernTheme.ACCENT};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 8px;
            background-color: {ModernTheme.BG_MEDIUM};
        }}
        
        QTabBar::tab {{
            background-color: {ModernTheme.BG_LIGHT};
            color: {ModernTheme.TEXT_SECONDARY};
            border: 1px solid {ModernTheme.BORDER};
            border-bottom: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 10px 20px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {ModernTheme.ACCENT};
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        QTabBar::tab:hover {{
            background-color: {ModernTheme.BG_HOVER};
        }}
        """
    
    @staticmethod
    def get_card_style():
        """Get style for card-like containers."""
        return f"""
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 12px;
            padding: 20px;
        """
    
    @staticmethod
    def get_panel_style():
        """Get style for side panels."""
        return f"""
            background-color: {ModernTheme.BG_MEDIUM};
            border-right: 1px solid {ModernTheme.BORDER};
        """
