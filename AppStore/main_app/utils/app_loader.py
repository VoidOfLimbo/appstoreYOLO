"""Dynamic app loader for sub-applications.

This module handles the discovery and loading of sub-applications from the apps/ directory.
"""

import os
import sys
import importlib.util
from typing import List, Dict, Type, Optional
from main_app.utils.base_app import BaseApp


class AppLoader:
    """Dynamically loads sub-applications from the apps directory."""
    
    def __init__(self, apps_dir: str):
        """Initialize the app loader.
        
        Args:
            apps_dir: Path to the apps directory
        """
        self.apps_dir = apps_dir
        self.loaded_apps: Dict[str, BaseApp] = {}
    
    def discover_apps(self) -> List[str]:
        """Discover all available apps in the apps directory.
        
        Returns:
            List of app directory names
        """
        if not os.path.exists(self.apps_dir):
            print(f"Apps directory not found: {self.apps_dir}")
            return []
        
        apps = []
        for item in os.listdir(self.apps_dir):
            item_path = os.path.join(self.apps_dir, item)
            if os.path.isdir(item_path) and not item.startswith('__'):
                # Check if the app has the required files
                detector_file = os.path.join(item_path, f"{item}.py")
                config_file = os.path.join(item_path, "config.json")
                
                if os.path.exists(detector_file) or os.path.exists(config_file):
                    apps.append(item)
        
        return apps
    
    def load_app(self, app_name: str) -> Optional[BaseApp]:
        """Load a specific application by name.
        
        Args:
            app_name: Name of the app to load
            
        Returns:
            Instance of the loaded app, or None if loading failed
        """
        if app_name in self.loaded_apps:
            return self.loaded_apps[app_name]
        
        app_path = os.path.join(self.apps_dir, app_name)
        module_file = os.path.join(app_path, f"{app_name}.py")
        
        if not os.path.exists(module_file):
            print(f"Module file not found: {module_file}")
            return None
        
        try:
            # Load the module dynamically
            spec = importlib.util.spec_from_file_location(app_name, module_file)
            if spec is None or spec.loader is None:
                print(f"Failed to create module spec for {app_name}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[app_name] = module
            spec.loader.exec_module(module)
            
            # Find the app class (should be a subclass of BaseApp)
            app_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseApp) and 
                    attr is not BaseApp):
                    app_class = attr
                    break
            
            if app_class is None:
                print(f"No BaseApp subclass found in {app_name}")
                return None
            
            # Instantiate the app
            app_instance = app_class(app_path)
            
            # Initialize the app
            if app_instance.initialize():
                self.loaded_apps[app_name] = app_instance
                print(f"Successfully loaded app: {app_name}")
                return app_instance
            else:
                print(f"Failed to initialize app: {app_name}")
                return None
                
        except Exception as e:
            print(f"Error loading app {app_name}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def load_all_apps(self) -> Dict[str, BaseApp]:
        """Load all discovered applications.
        
        Returns:
            Dictionary of loaded apps {app_name: app_instance}
        """
        app_names = self.discover_apps()
        print(f"Discovered apps: {app_names}")
        
        for app_name in app_names:
            self.load_app(app_name)
        
        return self.loaded_apps
    
    def unload_app(self, app_name: str):
        """Unload a specific application.
        
        Args:
            app_name: Name of the app to unload
        """
        if app_name in self.loaded_apps:
            app = self.loaded_apps[app_name]
            app.cleanup()
            del self.loaded_apps[app_name]
            print(f"Unloaded app: {app_name}")
    
    def unload_all_apps(self):
        """Unload all loaded applications."""
        app_names = list(self.loaded_apps.keys())
        for app_name in app_names:
            self.unload_app(app_name)
    
    def get_app(self, app_name: str) -> Optional[BaseApp]:
        """Get a loaded app by name.
        
        Args:
            app_name: Name of the app
            
        Returns:
            The app instance, or None if not loaded
        """
        return self.loaded_apps.get(app_name)
    
    def get_all_apps(self) -> Dict[str, BaseApp]:
        """Get all loaded apps.
        
        Returns:
            Dictionary of all loaded apps
        """
        return self.loaded_apps
