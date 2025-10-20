"""Version management utilities.

This module provides version comparison and tracking functionality.
"""

import os
from typing import Tuple, Optional


class VersionManager:
    """Manages application version information."""
    
    def __init__(self, version_file: str):
        """Initialize the version manager.
        
        Args:
            version_file: Path to the version.txt file
        """
        self.version_file = version_file
        self.current_version = self.read_version()
    
    def read_version(self) -> str:
        """Read the current version from the version file.
        
        Returns:
            Version string (e.g., "1.0.0")
        """
        if os.path.exists(self.version_file):
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                print(f"Error reading version file: {e}")
                return "0.0.0"
        return "0.0.0"
    
    def write_version(self, version: str) -> bool:
        """Write a new version to the version file.
        
        Args:
            version: Version string to write
            
        Returns:
            True if successful
        """
        try:
            with open(self.version_file, 'w', encoding='utf-8') as f:
                f.write(version)
            self.current_version = version
            return True
        except Exception as e:
            print(f"Error writing version file: {e}")
            return False
    
    @staticmethod
    def parse_version(version: str) -> Tuple[int, int, int]:
        """Parse a version string into tuple of integers.
        
        Args:
            version: Version string (e.g., "1.2.3")
            
        Returns:
            Tuple of (major, minor, patch)
        """
        try:
            parts = version.split('.')
            major = int(parts[0]) if len(parts) > 0 else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            patch = int(parts[2]) if len(parts) > 2 else 0
            return (major, minor, patch)
        except (ValueError, IndexError):
            return (0, 0, 0)
    
    @staticmethod
    def compare_versions(version1: str, version2: str) -> int:
        """Compare two version strings.
        
        Args:
            version1: First version string
            version2: Second version string
            
        Returns:
            -1 if version1 < version2
             0 if version1 == version2
             1 if version1 > version2
        """
        v1 = VersionManager.parse_version(version1)
        v2 = VersionManager.parse_version(version2)
        
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        else:
            return 0
    
    def is_newer_version(self, new_version: str) -> bool:
        """Check if a version is newer than the current version.
        
        Args:
            new_version: Version to check
            
        Returns:
            True if new_version is newer
        """
        return self.compare_versions(new_version, self.current_version) > 0
    
    def should_update(self, new_version: str) -> Tuple[bool, str]:
        """Determine if an update should be performed.
        
        Args:
            new_version: New version being installed
            
        Returns:
            Tuple of (should_update, reason)
        """
        comparison = self.compare_versions(new_version, self.current_version)
        
        if comparison > 0:
            return (True, f"Updating from {self.current_version} to {new_version}")
        elif comparison < 0:
            return (False, f"Installed version ({self.current_version}) is newer than {new_version}")
        else:
            return (False, f"Version {new_version} is already installed")
    
    def get_version_info(self) -> dict:
        """Get detailed version information.
        
        Returns:
            Dictionary with version details
        """
        major, minor, patch = self.parse_version(self.current_version)
        return {
            'version': self.current_version,
            'major': major,
            'minor': minor,
            'patch': patch,
            'file': self.version_file
        }


# Convenience function for checking installed version
def get_installed_version(install_path: str) -> Optional[str]:
    """Get the version of an installed application.
    
    Args:
        install_path: Path to the installation directory
        
    Returns:
        Version string if found, None otherwise
    """
    version_file = os.path.join(install_path, 'config', 'version.txt')
    if os.path.exists(version_file):
        try:
            with open(version_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception:
            pass
    return None


# Example usage
if __name__ == "__main__":
    # Test version comparison
    vm = VersionManager("version.txt")
    
    print(f"Current version: {vm.current_version}")
    print(f"Version info: {vm.get_version_info()}")
    
    # Test comparisons
    test_versions = ["0.9.0", "1.0.0", "1.0.1", "1.1.0", "2.0.0"]
    for v in test_versions:
        should_update, reason = vm.should_update(v)
        print(f"{v}: {should_update} - {reason}")
