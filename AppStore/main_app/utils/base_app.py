"""Base class for all sub-applications.

This module provides a common interface for all pluggable sub-applications.
Each sub-app should inherit from BaseApp and implement the required methods.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import os
from PyQt5.QtWidgets import QWidget


class BaseApp(ABC):
    """Abstract base class for sub-applications.
    
    All sub-apps must inherit from this class and implement the required methods.
    This ensures a consistent interface across all pluggable applications.
    """
    
    def __init__(self, app_path: str):
        """Initialize the base application.
        
        Args:
            app_path: Path to the application directory
        """
        self.app_path = app_path
        self.config = self._load_config()
        self.name = self.config.get('name', 'Modal Builder App')
        self.version = self.config.get('version', '1.0.0')
        self.description = self.config.get('description', '')
        self.enabled = self.config.get('enabled', True)
        self._widget: Optional[QWidget] = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json in the app directory.
        
        Returns:
            Dictionary containing the app configuration
        """
        config_path = os.path.join(self.app_path, 'config.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config for {self.app_path}: {e}")
                return {}
        return {}
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the application.
        
        This method is called once when the app is loaded.
        Use it to set up resources, load models, etc.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def create_widget(self) -> QWidget:
        """Create and return the main widget for this application.
        
        This widget will be displayed in the main UI when the app is selected.
        
        Returns:
            QWidget instance representing the app's UI
        """
        pass
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process input data.
        
        This is the main processing method for the application.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed output data
        """
        pass
    
    def cleanup(self):
        """Clean up resources before the app is unloaded.
        
        Override this method to release resources, close connections, etc.
        """
        pass
    
    def get_widget(self) -> QWidget:
        """Get the app's widget, creating it if necessary.
        
        Returns:
            The app's widget instance
        """
        if self._widget is None:
            self._widget = self.create_widget()
        return self._widget
    
    def is_enabled(self) -> bool:
        """Check if the application is enabled.
        
        Returns:
            True if enabled, False otherwise
        """
        return self.enabled
    
    def get_info(self) -> Dict[str, str]:
        """Get application information.
        
        Returns:
            Dictionary with app name, version, and description
        """
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'path': self.app_path
        }
