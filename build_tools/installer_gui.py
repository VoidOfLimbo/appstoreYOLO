
import sys
import os
import subprocess
import shutil
import zipfile
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QWizard, QWizardPage, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QCheckBox, QTextEdit, QProgressBar, QFileDialog,
                             QMessageBox, QGroupBox, QRadioButton)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon

class SystemCheckThread(QThread):
    """Thread for checking system requirements."""
    update_status = pyqtSignal(str, bool)  # message, success
    finished_check = pyqtSignal(dict)  # results dictionary
    
    def run(self):
        results = {}
        
        # Check Python
        self.update_status.emit("Checking Python installation...", True)
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            version = result.stdout.strip()
            if "Python 3.10" in version or "Python 3.11" in version:
                results['python'] = {'installed': True, 'version': version}
                self.update_status.emit(f"✓ {version}", True)
            else:
                results['python'] = {'installed': False, 'version': version}
                self.update_status.emit(f"✗ {version} (Need 3.10 or 3.11)", False)
        except Exception as e:
            results['python'] = {'installed': False, 'error': str(e)}
            self.update_status.emit("✗ Python not found", False)
        
        # Check NVIDIA Driver
        self.update_status.emit("Checking NVIDIA drivers...", True)
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                driver_line = [l for l in lines if 'Driver Version' in l]
                if driver_line:
                    results['nvidia'] = {'installed': True, 'info': driver_line[0].strip()}
                    self.update_status.emit("✓ NVIDIA drivers detected", True)
                else:
                    results['nvidia'] = {'installed': True, 'info': 'Detected'}
                    self.update_status.emit("✓ NVIDIA drivers detected", True)
            else:
                results['nvidia'] = {'installed': False}
                self.update_status.emit("✗ NVIDIA drivers not found", False)
        except Exception:
            results['nvidia'] = {'installed': False}
            self.update_status.emit("✗ NVIDIA drivers not found", False)
        
        # Check disk space (need at least 5GB)
        self.update_status.emit("Checking disk space...", True)
        try:
            import shutil
            total, used, free = shutil.disk_usage("C:\\")
            free_gb = free / (1024**3)
            if free_gb >= 5:
                results['disk'] = {'installed': True, 'free_gb': free_gb}
                self.update_status.emit(f"✓ {free_gb:.1f} GB free", True)
            else:
                results['disk'] = {'installed': False, 'free_gb': free_gb}
                self.update_status.emit(f"✗ Only {free_gb:.1f} GB free (need 5GB)", False)
        except Exception as e:
            results['disk'] = {'installed': False, 'error': str(e)}
            self.update_status.emit("✗ Could not check disk space", False)
        
        self.finished_check.emit(results)


class InstallThread(QThread):
    """Thread for performing installation."""
    update_progress = pyqtSignal(int, str)  # progress, message
    finished_install = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, install_path, create_shortcuts, install_deps):
        super().__init__()
        self.install_path = install_path
        self.create_shortcuts = create_shortcuts
        self.install_deps = install_deps
    
    def run(self):
        try:
            # Create installation directory
            self.update_progress.emit(5, "Creating installation directory...")
            os.makedirs(self.install_path, exist_ok=True)
            
            # Extract embedded files
            self.update_progress.emit(10, "Extracting application files...")
            self.extract_application_files()
            
            if self.install_deps:
                # Create virtual environment
                self.update_progress.emit(20, "Creating Python virtual environment...")
                venv_path = os.path.join(self.install_path, ".venv")
                subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
                
                # Upgrade pip
                self.update_progress.emit(30, "Upgrading pip...")
                pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
                subprocess.run([pip_exe, "install", "--upgrade", "pip"], check=True)
                
                # Install PyTorch with CUDA
                self.update_progress.emit(40, "Installing PyTorch with CUDA (this may take a while)...")
                subprocess.run([
                    pip_exe, "install", 
                    "torch", "torchvision", 
                    "--index-url", "https://download.pytorch.org/whl/cu124"
                ], check=True)
                
                # Install other requirements
                self.update_progress.emit(70, "Installing other dependencies...")
                req_file = os.path.join(self.install_path, "requirements.txt")
                subprocess.run([pip_exe, "install", "-r", req_file], check=True)
            
            # Create launcher script
            self.update_progress.emit(85, "Creating launcher...")
            self.create_launcher()
            
            # Create shortcuts
            if self.create_shortcuts:
                self.update_progress.emit(90, "Creating desktop shortcut...")
                self.create_desktop_shortcut()
            
            self.update_progress.emit(100, "Installation complete!")
            self.finished_install.emit(True, "Installation completed successfully!")
            
        except Exception as e:
            self.finished_install.emit(False, f"Installation failed: {str(e)}")
    
    def extract_application_files(self):
        """Extract application files to installation directory."""
        # Get the directory where this script is located
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Extract the embedded ZIP
        zip_path = os.path.join(base_path, "app_files.zip")
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.install_path)
        else:
            # Copy files from source
            src_files = ['main.py', 'requirements.txt', 'README.md']
            for file in src_files:
                src = os.path.join(base_path, file)
                if os.path.exists(src):
                    shutil.copy2(src, self.install_path)
            
            # Copy directories
            for dir_name in ['src', 'config', 'assets']:
                src_dir = os.path.join(base_path, dir_name)
                if os.path.exists(src_dir):
                    dst_dir = os.path.join(self.install_path, dir_name)
                    if os.path.exists(dst_dir):
                        shutil.rmtree(dst_dir)
                    shutil.copytree(src_dir, dst_dir)
            
            # Create empty directories
            for dir_name in ['logs', 'output']:
                os.makedirs(os.path.join(self.install_path, dir_name), exist_ok=True)
    
    def create_launcher(self):
        """Create launcher batch file."""
        launcher_path = os.path.join(self.install_path, "TensorRT_Converter.bat")
        with open(launcher_path, 'w') as f:
            f.write(f"""@echo off
cd /d "{self.install_path}"
call .venv\\Scripts\\activate.bat
python main.py
pause
""")
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut."""
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "TensorRT Converter.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = os.path.join(self.install_path, "TensorRT_Converter.bat")
            shortcut.WorkingDirectory = self.install_path
            shortcut.IconLocation = os.path.join(self.install_path, "assets", "icon.ico")
            shortcut.Description = "TensorRT Model Converter"
            shortcut.save()
        except Exception as e:
            print(f"Could not create shortcut: {e}")


class WelcomePage(QWizardPage):
    """Welcome page."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Welcome to TensorRT Converter Setup")
        
        layout = QVBoxLayout()
        
        # Welcome text
        welcome_text = QLabel(
            "<h2>Welcome!</h2>"
            "<p>This wizard will guide you through the installation of "
            "<b>TensorRT Model Converter</b>.</p>"
            "<p>This application allows you to convert YOLO models to TensorRT "
            "engine format for optimized inference.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Drag & drop model conversion</li>"
            "<li>Support for ONNX, TorchScript, OpenVINO export</li>"
            "<li>Automatic GPU detection and optimization</li>"
            "<li>Batch processing support</li>"
            "</ul>"
        )
        welcome_text.setWordWrap(True)
        layout.addWidget(welcome_text)
        
        layout.addStretch()
        self.setLayout(layout)


class SystemCheckPage(QWizardPage):
    """System requirements check page."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("System Requirements Check")
        self.setSubTitle("Checking your system for required components...")
        
        layout = QVBoxLayout()
        
        # Status text area
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        layout.addWidget(self.status_text)
        
        # Requirements info
        req_group = QGroupBox("Requirements")
        req_layout = QVBoxLayout()
        req_layout.addWidget(QLabel("• Python 3.10 or 3.11"))
        req_layout.addWidget(QLabel("• NVIDIA GPU with drivers"))
        req_layout.addWidget(QLabel("• At least 5 GB free disk space"))
        req_layout.addWidget(QLabel("• Internet connection (for first-time setup)"))
        req_group.setLayout(req_layout)
        layout.addWidget(req_group)
        
        # Results
        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.check_results = {}
    
    def initializePage(self):
        """Run system checks when page is shown."""
        self.status_text.clear()
        self.status_text.append("Starting system check...\n")
        
        # Start check thread
        self.check_thread = SystemCheckThread()
        self.check_thread.update_status.connect(self.update_status)
        self.check_thread.finished_check.connect(self.check_finished)
        self.check_thread.start()
    
    def update_status(self, message, success):
        """Update status text."""
        self.status_text.append(message)
    
    def check_finished(self, results):
        """Handle check completion."""
        self.check_results = results
        
        all_ok = all(r.get('installed', False) for r in results.values())
        
        if all_ok:
            self.results_label.setText(
                '<span style="color: green; font-weight: bold;">✓ All requirements met!</span>'
            )
        else:
            missing = []
            if not results.get('python', {}).get('installed'):
                missing.append("Python 3.10/3.11")
            if not results.get('nvidia', {}).get('installed'):
                missing.append("NVIDIA drivers")
            if not results.get('disk', {}).get('installed'):
                missing.append("Sufficient disk space")
            
            self.results_label.setText(
                f'<span style="color: orange; font-weight: bold;">⚠ Missing: {", ".join(missing)}</span><br>'
                f'<span style="color: #666;">You can continue, but some features may not work.</span>'
            )
        
        self.completeChanged.emit()
    
    def isComplete(self):
        """Allow proceeding even if some checks fail."""
        return len(self.check_results) > 0


class InstallOptionsPage(QWizardPage):
    """Installation options page."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Installation Options")
        self.setSubTitle("Choose where and how to install TensorRT Converter")
        
        layout = QVBoxLayout()
        
        # Installation path
        path_group = QGroupBox("Installation Location")
        path_layout = QHBoxLayout()
        
        self.path_edit = QLineEdit()
        default_path = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 
                                   'TensorRT_Converter')
        self.path_edit.setText(default_path)
        path_layout.addWidget(self.path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(browse_btn)
        
        path_group.setLayout(path_layout)
        layout.addWidget(path_group)
        
        # Installation options
        options_group = QGroupBox("Installation Options")
        options_layout = QVBoxLayout()
        
        self.install_deps_check = QCheckBox("Install Python dependencies (PyTorch, TensorRT, etc.)")
        self.install_deps_check.setChecked(True)
        self.install_deps_check.setToolTip(
            "Downloads and installs all required Python packages.\n"
            "Requires internet connection. May take 10-20 minutes."
        )
        options_layout.addWidget(self.install_deps_check)
        
        self.shortcuts_check = QCheckBox("Create desktop shortcut")
        self.shortcuts_check.setChecked(True)
        options_layout.addWidget(self.shortcuts_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Space info
        self.space_label = QLabel()
        self.update_space_info()
        layout.addWidget(self.space_label)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Register fields
        self.registerField("installPath*", self.path_edit)
        self.registerField("installDeps", self.install_deps_check)
        self.registerField("createShortcuts", self.shortcuts_check)
    
    def browse_path(self):
        """Browse for installation directory."""
        path = QFileDialog.getExistingDirectory(
            self, "Select Installation Directory",
            self.path_edit.text()
        )
        if path:
            self.path_edit.setText(path)
            self.update_space_info()
    
    def update_space_info(self):
        """Update disk space information."""
        try:
            path = self.path_edit.text()
            if not path:
                path = "C:\\"
            else:
                # Get drive letter
                drive = os.path.splitdrive(path)[0]
                if not drive:
                    drive = "C:\\"
                else:
                    drive = drive + "\\"
            
            total, used, free = shutil.disk_usage(drive)
            free_gb = free / (1024**3)
            
            if self.install_deps_check.isChecked():
                required = 5.0
            else:
                required = 0.1
            
            if free_gb >= required:
                color = "green"
                icon = "✓"
            else:
                color = "red"
                icon = "✗"
            
            self.space_label.setText(
                f'<span style="color: {color};">{icon} Available space: {free_gb:.1f} GB '
                f'(Required: {required:.1f} GB)</span>'
            )
        except Exception:
            self.space_label.setText("")


class InstallationPage(QWizardPage):
    """Installation progress page."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Installing")
        self.setSubTitle("Please wait while TensorRT Converter is being installed...")
        
        layout = QVBoxLayout()
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        layout.addWidget(self.progress)
        
        # Status label
        self.status_label = QLabel("Preparing installation...")
        layout.addWidget(self.status_label)
        
        # Log text
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.install_success = False
    
    def initializePage(self):
        """Start installation when page is shown."""
        install_path = self.field("installPath")
        create_shortcuts = self.field("createShortcuts")
        install_deps = self.field("installDeps")
        
        self.log_text.clear()
        self.log_text.append(f"Installing to: {install_path}\n")
        
        # Start installation thread
        self.install_thread = InstallThread(install_path, create_shortcuts, install_deps)
        self.install_thread.update_progress.connect(self.update_progress)
        self.install_thread.finished_install.connect(self.install_finished)
        self.install_thread.start()
    
    def update_progress(self, value, message):
        """Update progress bar and message."""
        self.progress.setValue(value)
        self.status_label.setText(message)
        self.log_text.append(f"[{value}%] {message}")
    
    def install_finished(self, success, message):
        """Handle installation completion."""
        self.install_success = success
        
        if success:
            self.status_label.setText('<span style="color: green;">✓ Installation completed!</span>')
        else:
            self.status_label.setText(f'<span style="color: red;">✗ Installation failed</span>')
        
        self.log_text.append(f"\n{message}")
        self.completeChanged.emit()
    
    def isComplete(self):
        """Page is complete when installation finishes."""
        return self.install_success


class FinishPage(QWizardPage):
    """Completion page."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Installation Complete")
        
        layout = QVBoxLayout()
        
        self.message_label = QLabel()
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)
        
        self.launch_check = QCheckBox("Launch TensorRT Converter now")
        self.launch_check.setChecked(False)
        layout.addWidget(self.launch_check)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def initializePage(self):
        """Update completion message."""
        install_path = self.field("installPath")
        
        self.message_label.setText(
            "<h3>Setup completed successfully!</h3>"
            f"<p>TensorRT Converter has been installed to:<br>"
            f"<b>{install_path}</b></p>"
            "<p>You can now:</p>"
            "<ul>"
            "<li>Launch the application from the Start Menu</li>"
            "<li>Use the desktop shortcut (if created)</li>"
            f'<li>Run <code>{os.path.join(install_path, "TensorRT_Converter.bat")}</code></li>'
            "</ul>"
            "<p><b>Thank you for installing TensorRT Converter!</b></p>"
        )


class InstallerWizard(QWizard):
    """Main installer wizard."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("TensorRT Converter Setup")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setOption(QWizard.HaveHelpButton, False)
        self.setOption(QWizard.NoBackButtonOnStartPage, True)
        self.setOption(QWizard.NoBackButtonOnLastPage, True)
        self.setOption(QWizard.NoCancelButtonOnLastPage, True)
        self.setOption(QWizard.IndependentPages, False)
        self.setMinimumSize(700, 500)
        self.setMaximumSize(900, 700)
        
        # Ensure pages stay in same window
        self.setModal(True)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        # Create and add pages with explicit parent
        self.welcome_page = WelcomePage(self)
        self.system_page = SystemCheckPage(self)
        self.options_page = InstallOptionsPage(self)
        self.install_page = InstallationPage(self)
        self.finish_page = FinishPage(self)
        
        # Add pages
        self.addPage(self.welcome_page)
        self.addPage(self.system_page)
        self.addPage(self.options_page)
        self.addPage(self.install_page)
        self.addPage(self.finish_page)
        
        # Set button text
        self.setButtonText(QWizard.NextButton, "Next >")
        self.setButtonText(QWizard.BackButton, "< Back")
        self.setButtonText(QWizard.FinishButton, "Finish")
        self.setButtonText(QWizard.CancelButton, "Cancel")
    
    def accept(self):
        """Handle wizard completion."""
        # Check if user wants to launch
        finish_page = self.page(self.pageIds()[-1])
        if hasattr(finish_page, 'launch_check') and finish_page.launch_check.isChecked():
            install_path = self.field("installPath")
            launcher = os.path.join(install_path, "TensorRT_Converter.bat")
            if os.path.exists(launcher):
                subprocess.Popen(launcher, shell=True)
        
        super().accept()


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    wizard = InstallerWizard()
    wizard.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
