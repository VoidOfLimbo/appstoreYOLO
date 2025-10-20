"""Modern UI Theme Configuration.

This module provides a modern dark theme with consistent styling.
"""

class ModernTheme:
    """Modern dark theme with accent colors."""
    
    # Main colors
    PRIMARY = "#2C3E50"
    SECONDARY = "#34495E"
    ACCENT = "#4A9EFF"
    ACCENT_HOVER = "#5AADFF"
    SUCCESS = "#27AE60"
    WARNING = "#F39C12"
    DANGER = "#E74C3C"
    
    # Background colors
    BG_DARK = "#1A1A1A"
    BG_MEDIUM = "#222222"
    BG_LIGHT = "#2A2A2A"
    BG_HOVER = "#333333"
    BG_PANEL = "#1E1E1E"
    
    # Text colors
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#CCCCCC"
    TEXT_DISABLED = "#808080"
    TEXT_MUTED = "#999999"
    
    # Border colors
    BORDER = "#3A3A3A"
    BORDER_LIGHT = "#4A4A4A"
    
    
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
            background-color: transparent;
            color: {ModernTheme.TEXT_PRIMARY};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 10pt;
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {ModernTheme.ACCENT};
            color: #FFFFFF;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 11pt;
            min-height: 32px;
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
            background-color: {ModernTheme.BG_LIGHT};
            color: {ModernTheme.TEXT_PRIMARY};
            border: 1px solid {ModernTheme.BORDER};
        }}
        
        QPushButton[class="secondary"]:hover {{
            background-color: {ModernTheme.BG_HOVER};
            border: 1px solid {ModernTheme.ACCENT};
        }}
        
        /* Success Button */
        QPushButton[class="success"] {{
            background-color: {ModernTheme.SUCCESS};
            color: #FFFFFF;
        }}
        
        /* Warning Button */
        QPushButton[class="warning"] {{
            background-color: {ModernTheme.WARNING};
            color: #FFFFFF;
        }}
        
        /* Danger Button */
        QPushButton[class="danger"] {{
            background-color: {ModernTheme.DANGER};
            color: #FFFFFF;
        }}
        
        /* Labels */
        QLabel {{
            color: {ModernTheme.TEXT_PRIMARY};
            background-color: transparent;
        }}
        
        QLabel[class="title"] {{
            font-size: 28pt;
            font-weight: bold;
            color: {ModernTheme.ACCENT};
        }}
        
        QLabel[class="subtitle"] {{
            font-size: 12pt;
            color: {ModernTheme.TEXT_SECONDARY};
            font-weight: 500;
        }}
        
        QLabel[class="header"] {{
            font-size: 11pt;
            font-weight: 600;
            color: {ModernTheme.TEXT_SECONDARY};
            padding: 4px;
        }}
        
        QLabel[class="muted"] {{
            color: {ModernTheme.TEXT_MUTED};
        }}
        
        /* Text Edit */
        QTextEdit {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 4px;
            padding: 4px;
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        /* Line Edit */
        QLineEdit {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 4px;
            padding: 4px;
            color: {ModernTheme.TEXT_PRIMARY};
            font-size: 10pt;
        }}
        
        QLineEdit:focus {{
            border: 2px solid {ModernTheme.ACCENT};
        }}
        
        /* Combo Box */
        QComboBox {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 4px;
            padding: 4px 8px;
            color: {ModernTheme.TEXT_PRIMARY};
            min-height: 24px;
        }}
        
        QComboBox:hover {{
            border: 1px solid {ModernTheme.ACCENT};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 24px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            selection-background-color: {ModernTheme.ACCENT};
            selection-color: #FFFFFF;
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        /* Spin Box */
        QSpinBox {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 4px;
            padding: 4px;
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        QSpinBox:focus {{
            border: 2px solid {ModernTheme.ACCENT};
        }}
        
        /* Check Box */
        QCheckBox {{
            color: {ModernTheme.TEXT_PRIMARY};
            spacing: 4px;
        }}
        
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 2px;
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
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 8px;
            font-weight: bold;
            color: {ModernTheme.TEXT_PRIMARY};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 4px;
            background-color: {ModernTheme.BG_DARK};
            color: {ModernTheme.ACCENT};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            background-color: {ModernTheme.BG_MEDIUM};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 4px;
            text-align: center;
            color: {ModernTheme.TEXT_PRIMARY};
            height: 20px;
        }}
        
        QProgressBar::chunk {{
            background-color: {ModernTheme.ACCENT};
            border-radius: 4px;
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: transparent;
            width: 8px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {ModernTheme.BORDER_LIGHT};
            border-radius: 4px;
            min-height: 24px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {ModernTheme.ACCENT};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: transparent;
            height: 8px;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {ModernTheme.BORDER_LIGHT};
            border-radius: 4px;
            min-width: 24px;
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
            background-color: {ModernTheme.BG_PANEL};
            color: {ModernTheme.TEXT_SECONDARY};
            border-top: 1px solid {ModernTheme.BORDER};
            font-size: 9pt;
        }}
        
        /* Tool Tip */
        QToolTip {{
            background-color: {ModernTheme.BG_LIGHT};
            color: {ModernTheme.TEXT_PRIMARY};
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 4px;
            padding: 4px;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {ModernTheme.BORDER};
            border-radius: 4px;
            background-color: {ModernTheme.BG_MEDIUM};
        }}
        
        QTabBar::tab {{
            background-color: {ModernTheme.BG_LIGHT};
            color: {ModernTheme.TEXT_SECONDARY};
            border: 1px solid {ModernTheme.BORDER};
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 8px 16px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {ModernTheme.ACCENT};
            color: #FFFFFF;
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
            border-radius: 4px;
            padding: 8px;
        """
    
    @staticmethod
    def get_panel_style():
        """Get style for side panels."""
        return f"""
            background-color: {ModernTheme.BG_PANEL};
            border-right: 1px solid {ModernTheme.BORDER};
        """


