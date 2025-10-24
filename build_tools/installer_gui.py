import sys
import os
import subprocess
import shutil
import zipfile
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QTextEdit,
    QProgressBar,
    QFileDialog,
    QMessageBox,
    QGroupBox,
    QRadioButton,
)
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
            result = subprocess.run(
                [sys.executable, "--version"], capture_output=True, text=True
            )
            version_full = result.stdout.strip()
            # Extract version number (e.g., "Python 3.10.11" -> "3.10.11")
            version_str = version_full.replace("Python ", "")
            version_parts = version_str.split(".")

            if len(version_parts) >= 2:
                major = int(version_parts[0])
                minor = int(version_parts[1])

                if major == 3 and minor in [10, 11]:
                    results["python"] = {"installed": True, "version": version_full}
                    self.update_status.emit(
                        f"✓ Required: Python 3.10 or 3.11 ... Found: {version_full}",
                        True,
                    )
                elif major == 3 and minor >= 8:
                    results["python"] = {
                        "installed": True,
                        "version": version_full,
                        "warning": True,
                    }
                    self.update_status.emit(
                        f"⚠ Required: Python 3.10 or 3.11 ... Found: {version_full}",
                        True,
                    )
                else:
                    results["python"] = {"installed": False, "version": version_full}
                    self.update_status.emit(
                        f"✗ Required: Python 3.10 or 3.11 ... Found: {version_full}",
                        False,
                    )
            else:
                results["python"] = {"installed": False, "version": version_full}
                self.update_status.emit(
                    f"✗ Required: Python 3.10 or 3.11 ... Found: {version_full}", False
                )
        except Exception as e:
            results["python"] = {"installed": False, "error": str(e)}
            self.update_status.emit("✗ Python not found", False)

        # Check NVIDIA Driver
        self.update_status.emit("Checking NVIDIA drivers...", True)
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split("\n")
                driver_line = [l for l in lines if "Driver Version" in l]
                if driver_line:
                    results["nvidia"] = {
                        "installed": True,
                        "info": driver_line[0].strip(),
                    }
                    self.update_status.emit("✓ NVIDIA drivers detected", True)
                else:
                    results["nvidia"] = {"installed": True, "info": "Detected"}
                    self.update_status.emit("✓ NVIDIA drivers detected", True)
            else:
                results["nvidia"] = {"installed": False}
                self.update_status.emit("✗ NVIDIA drivers not found", False)
        except Exception:
            results["nvidia"] = {"installed": False}
            self.update_status.emit("✗ NVIDIA drivers not found", False)

        # Check disk space (need at least 5GB)
        self.update_status.emit("Checking disk space...", True)
        try:
            import shutil

            total, used, free = shutil.disk_usage("C:\\")
            free_gb = free / (1024**3)
            if free_gb >= 5:
                results["disk"] = {"installed": True, "free_gb": free_gb}
                self.update_status.emit(f"✓ {free_gb:.1f} GB free", True)
            else:
                results["disk"] = {"installed": False, "free_gb": free_gb}
                self.update_status.emit(
                    f"✗ Only {free_gb:.1f} GB free (need 5GB)", False
                )
        except Exception as e:
            results["disk"] = {"installed": False, "error": str(e)}
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
                self.update_progress.emit(
                    40, "Installing PyTorch with CUDA (this may take a while)..."
                )
                subprocess.run(
                    [
                        pip_exe,
                        "install",
                        "torch",
                        "torchvision",
                        "--index-url",
                        "https://download.pytorch.org/whl/cu124",
                    ],
                    check=True,
                )

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
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Extract the embedded ZIP
        zip_path = os.path.join(base_path, "app_files.zip")
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.install_path)
        else:
            # Copy files from source
            src_files = ["main.py", "requirements.txt", "README.md"]
            for file in src_files:
                src = os.path.join(base_path, file)
                if os.path.exists(src):
                    shutil.copy2(src, self.install_path)

            # Copy directories
            for dir_name in ["src", "config", "assets"]:
                src_dir = os.path.join(base_path, dir_name)
                if os.path.exists(src_dir):
                    dst_dir = os.path.join(self.install_path, dir_name)
                    if os.path.exists(dst_dir):
                        shutil.rmtree(dst_dir)
                    shutil.copytree(src_dir, dst_dir)

            # Create empty directories
            for dir_name in ["logs", "output"]:
                os.makedirs(os.path.join(self.install_path, dir_name), exist_ok=True)

    def create_launcher(self):
        """Create launcher batch file."""
        launcher_path = os.path.join(self.install_path, "TensorRT_Converter.bat")
        with open(launcher_path, "w") as f:
            f.write(
                f"""@echo off
cd /d "{self.install_path}"
call .venv\\Scripts\\activate.bat
python main.py
pause
"""
            )

    def create_desktop_shortcut(self):
        """Create desktop shortcut."""
        try:
            import winshell
            from win32com.client import Dispatch

            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "TensorRT Converter.lnk")

            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = os.path.join(
                self.install_path, "TensorRT_Converter.bat"
            )
            shortcut.WorkingDirectory = self.install_path
            shortcut.IconLocation = os.path.join(
                self.install_path, "assets", "icon.ico"
            )
            shortcut.Description = "TensorRT Model Converter"
            shortcut.save()
        except Exception as e:
            print(f"Could not create shortcut: {e}")


class WelcomePage(QWidget):
    """Welcome page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensure this is NOT a window
        self.setWindowFlags(Qt.Widget)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

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


class SystemCheckPage(QWidget):
    """System requirements check page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensure this is NOT a window
        self.setWindowFlags(Qt.Widget)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        layout = QVBoxLayout()

        # Title
        title = QLabel("<h2>System Requirements Check</h2>")
        layout.addWidget(title)

        subtitle = QLabel("Checking your system for required components...")
        layout.addWidget(subtitle)

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

    def start_check(self):
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

        all_ok = all(r.get("installed", False) for r in results.values())

        if all_ok:
            self.results_label.setText(
                '<span style="color: green; font-weight: bold;">✓ All requirements met!</span>'
            )
        else:
            missing = []
            if not results.get("python", {}).get("installed"):
                missing.append("Python 3.10/3.11")
            if not results.get("nvidia", {}).get("installed"):
                missing.append("NVIDIA drivers")
            if not results.get("disk", {}).get("installed"):
                missing.append("Sufficient disk space")

            self.results_label.setText(
                f'<span style="color: orange; font-weight: bold;">⚠ Missing: {", ".join(missing)}</span><br>'
                f'<span style="color: #666;">You can continue, but some features may not work.</span>'
            )


class InstallOptionsPage(QWidget):
    """Installation options page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensure this is NOT a window
        self.setWindowFlags(Qt.Widget)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        layout = QVBoxLayout()

        # Title
        title = QLabel("<h2>Installation Options</h2>")
        layout.addWidget(title)

        subtitle = QLabel("Choose where and how to install TensorRT Converter")
        layout.addWidget(subtitle)

        # Installation path
        path_group = QGroupBox("Installation Location")
        path_layout = QHBoxLayout()

        self.path_edit = QLineEdit()
        default_path = os.path.join(
            os.environ.get("PROGRAMFILES", "C:\\Program Files"), "TensorRT_Converter"
        )
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

        self.install_deps_check = QCheckBox(
            "Install Python dependencies (PyTorch, TensorRT, etc.)"
        )
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

    def browse_path(self):
        """Browse for installation directory."""
        path = QFileDialog.getExistingDirectory(
            self, "Select Installation Directory", self.path_edit.text()
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
                f"(Required: {required:.1f} GB)</span>"
            )
        except Exception:
            self.space_label.setText("")


class InstallationPage(QWidget):
    """Installation progress page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensure this is NOT a window
        self.setWindowFlags(Qt.Widget)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        layout = QVBoxLayout()

        # Title
        title = QLabel("<h2>Installing</h2>")
        layout.addWidget(title)

        subtitle = QLabel("Please wait while TensorRT Converter is being installed...")
        layout.addWidget(subtitle)

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

    def start_installation(self, install_path, install_deps, create_shortcuts):
        """Start installation when page is shown."""

        self.log_text.clear()
        self.log_text.append(f"Installing to: {install_path}\n")

        # Start installation thread
        self.install_thread = InstallThread(
            install_path, create_shortcuts, install_deps
        )
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
            self.status_label.setText(
                '<span style="color: green;">✓ Installation completed!</span>'
            )
        else:
            self.status_label.setText(
                f'<span style="color: red;">✗ Installation failed</span>'
            )

        self.log_text.append(f"\n{message}")
        # Enable next button when installation completes
        if hasattr(self.parent(), "next_button"):
            self.parent().next_button.setEnabled(True)


class FinishPage(QWidget):
    """Completion page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Ensure this is NOT a window
        self.setWindowFlags(Qt.Widget)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        layout = QVBoxLayout()

        # Title
        title = QLabel("<h2>Installation Complete</h2>")
        layout.addWidget(title)

        self.message_label = QLabel(
            "<p>TensorRT Model Converter has been successfully installed!</p>"
            "<p>You can now start converting YOLO models to TensorRT format for optimized inference.</p>"
        )
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        self.launch_check = QCheckBox("Launch TensorRT Converter now")
        self.launch_check.setChecked(False)
        layout.addWidget(self.launch_check)

        layout.addStretch()
        self.setLayout(layout)


class InstallerDialog(QDialog):
    """Main installer dialog with stacked pages."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("TensorRT Converter Setup")
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setMinimumSize(700, 500)
        self.setMaximumSize(900, 700)
        self.resize(800, 600)

        self.current_page = 0
        self.install_path = ""
        self.install_deps = True
        self.create_shortcuts = True

        # Main layout
        main_layout = QVBoxLayout()

        # Create stacked widget for pages
        self.pages = QStackedWidget(self)

        # Create pages - parent them to the stacked widget
        self.welcome_page = WelcomePage(self.pages)
        self.system_page = SystemCheckPage(self.pages)
        self.options_page = InstallOptionsPage(self.pages)
        self.install_page = InstallationPage(self.pages)
        self.finish_page = FinishPage(self.pages)

        # Add pages to stacked widget
        self.pages.addWidget(self.welcome_page)
        self.pages.addWidget(self.system_page)
        self.pages.addWidget(self.options_page)
        self.pages.addWidget(self.install_page)
        self.pages.addWidget(self.finish_page)

        main_layout.addWidget(self.pages)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.back_button = QPushButton("< Back")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)
        button_layout.addWidget(self.back_button)

        self.next_button = QPushButton("Next >")
        self.next_button.clicked.connect(self.go_next)
        button_layout.addWidget(self.next_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Show first page
        self.pages.setCurrentIndex(0)

    def go_next(self):
        """Navigate to next page."""
        if self.current_page == 0:
            # Welcome -> System Check
            # Explicitly hide current page to prevent two windows
            self.welcome_page.hide()
            self.current_page = 1
            self.back_button.setEnabled(True)
            self.pages.setCurrentIndex(1)
            # Show the new page
            self.system_page.show()
            # Process events to update UI
            QApplication.processEvents()
            # Start check after page is visible
            self.system_page.start_check()

        elif self.current_page == 1:
            # System Check -> Options
            self.system_page.hide()
            self.current_page = 2
            self.pages.setCurrentIndex(2)
            self.options_page.show()

        elif self.current_page == 2:
            # Options -> Installation
            self.install_path = self.options_page.path_edit.text()
            self.install_deps = self.options_page.deps_check.isChecked()
            self.create_shortcuts = self.options_page.shortcuts_check.isChecked()

            self.options_page.hide()
            self.current_page = 3
            self.pages.setCurrentIndex(3)
            self.install_page.show()
            self.next_button.setEnabled(False)
            self.back_button.setEnabled(False)
            self.install_page.start_installation(
                self.install_path, self.install_deps, self.create_shortcuts
            )

        elif self.current_page == 3:
            # Installation -> Finish
            self.install_page.hide()
            self.current_page = 4
            self.pages.setCurrentIndex(4)
            self.finish_page.show()
            self.next_button.setText("Finish")
            self.back_button.setEnabled(False)
            self.cancel_button.setEnabled(False)

        elif self.current_page == 4:
            # Finish - check if launch
            if self.finish_page.launch_check.isChecked():
                launcher = os.path.join(self.install_path, "TensorRT_Converter.bat")
                if os.path.exists(launcher):
                    subprocess.Popen(launcher, shell=True)
            self.accept()

    def go_back(self):
        """Navigate to previous page."""
        if self.current_page > 0:
            # Hide current page
            current_widget = self.pages.currentWidget()
            if current_widget:
                current_widget.hide()

            self.current_page -= 1
            self.pages.setCurrentIndex(self.current_page)

            # Show previous page
            previous_widget = self.pages.currentWidget()
            if previous_widget:
                previous_widget.show()

            if self.current_page == 0:
                self.back_button.setEnabled(False)


def main():
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    dialog = InstallerDialog()
    result = dialog.exec_()

    sys.exit(result)


if __name__ == "__main__":
    main()
