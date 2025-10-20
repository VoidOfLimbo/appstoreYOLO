"""
Training Application with Jupyter Notebook Integration

This application allows users to:
- Browse and launch Jupyter notebooks
- Monitor training progress
- Manage models and datasets
- Launch Jupyter Lab from within the app
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QListWidget, QTextEdit, QGroupBox, QFileDialog,
                             QListWidgetItem, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt, QProcess, QTimer
from PyQt5.QtGui import QFont
import sys
import os
from pathlib import Path
import subprocess

# Add parent directory to path to import BaseApp
sys.path.append(str(Path(__file__).parent.parent.parent))
from main_app.utils.base_app import BaseApp


class TrainingApp(BaseApp):
    """Training application with Jupyter notebook integration."""
    
    def __init__(self, app_path: str):
        super().__init__(app_path)
        self.jupyter_process = None
        self.jupyter_url = None
        self.notebooks_dir = Path(__file__).parent.parent.parent / 'notebooks'
        self.notebooks_dir.mkdir(exist_ok=True)
        
    def get_name(self):
        return "Training"
    
    def get_icon(self):
        return "🎓"
    
    def get_description(self):
        return "Train and fine-tune AI models using Jupyter notebooks"
    
    def initialize(self):
        """Initialize the training app."""
        print("Training app initialized")
        return True
    
    def create_widget(self):
        """Create the training interface."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("🎓 Model Training Center")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Train and fine-tune AI models using Jupyter notebooks. "
            "Launch Jupyter Lab to create and run interactive training workflows."
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("font-size: 14px; color: #7f8c8d; line-height: 1.6;")
        layout.addWidget(desc)
        
        # Splitter for notebooks and jupyter control
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Notebooks browser
        notebooks_group = self._create_notebooks_browser()
        splitter.addWidget(notebooks_group)
        
        # Right side - Jupyter control
        jupyter_group = self._create_jupyter_control()
        splitter.addWidget(jupyter_group)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter, 1)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        download_btn = QPushButton("📦 Download Models")
        download_btn.clicked.connect(self._download_models)
        download_btn.setMinimumHeight(45)
        actions_layout.addWidget(download_btn)
        
        open_folder_btn = QPushButton("📁 Open Notebooks Folder")
        open_folder_btn.clicked.connect(self._open_notebooks_folder)
        open_folder_btn.setMinimumHeight(45)
        actions_layout.addWidget(open_folder_btn)
        
        models_folder_btn = QPushButton("📂 Open Models Folder")
        models_folder_btn.clicked.connect(self._open_models_folder)
        models_folder_btn.setMinimumHeight(45)
        actions_layout.addWidget(models_folder_btn)
        
        layout.addLayout(actions_layout)
        
        widget.setLayout(layout)
        return widget
    
    def _create_notebooks_browser(self):
        """Create notebooks browser panel."""
        group = QGroupBox("📓 Available Notebooks")
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Notebooks list
        self.notebooks_list = QListWidget()
        self.notebooks_list.setStyleSheet("""
            QListWidget {
                background-color: #2C3E50;
                border: 2px solid #34495E;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 5px;
                margin: 2px;
            }
            QListWidget::item:hover {
                background-color: #34495E;
            }
            QListWidget::item:selected {
                background-color: #3498DB;
            }
        """)
        self._load_notebooks()
        layout.addWidget(self.notebooks_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        open_btn = QPushButton("Open in Jupyter")
        open_btn.clicked.connect(self._open_selected_notebook)
        open_btn.setMinimumHeight(40)
        btn_layout.addWidget(open_btn)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self._load_notebooks)
        refresh_btn.setMinimumHeight(40)
        btn_layout.addWidget(refresh_btn)
        
        layout.addLayout(btn_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_jupyter_control(self):
        """Create Jupyter control panel."""
        group = QGroupBox("⚙️ Jupyter Lab Control")
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Status
        self.status_label = QLabel("Status: Not Running")
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 12px;
                background-color: #34495E;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Control buttons
        self.start_btn = QPushButton("🚀 Start Jupyter Lab")
        self.start_btn.clicked.connect(self._start_jupyter)
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ECC71;
            }
        """)
        layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("🛑 Stop Jupyter Lab")
        self.stop_btn.clicked.connect(self._stop_jupyter)
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #999999;
            }
        """)
        layout.addWidget(self.stop_btn)
        
        # Output log
        log_label = QLabel("Jupyter Lab Output:")
        log_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(log_label)
        
        self.jupyter_log = QTextEdit()
        self.jupyter_log.setReadOnly(True)
        self.jupyter_log.setMaximumHeight(200)
        self.jupyter_log.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: 2px solid #34495E;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                color: #ECF0F1;
            }
        """)
        layout.addWidget(self.jupyter_log)
        
        # Info
        info = QLabel(
            "💡 Tip: Jupyter Lab will open in your default browser. "
            "You can create new notebooks or edit existing ones."
        )
        info.setWordWrap(True)
        info.setStyleSheet("""
            QLabel {
                padding: 12px;
                background-color: #34495E;
                border-radius: 6px;
                font-size: 12px;
                color: #95A5A6;
            }
        """)
        layout.addWidget(info)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
    
    def _load_notebooks(self):
        """Load available notebooks."""
        self.notebooks_list.clear()
        
        if not self.notebooks_dir.exists():
            return
        
        notebooks = sorted(self.notebooks_dir.glob('*.ipynb'))
        
        for notebook in notebooks:
            item = QListWidgetItem(f"📓 {notebook.stem}")
            item.setData(Qt.UserRole, str(notebook))
            self.notebooks_list.addItem(item)
        
        if not notebooks:
            item = QListWidgetItem("No notebooks found. Create one in Jupyter Lab!")
            item.setFlags(Qt.NoItemFlags)
            self.notebooks_list.addItem(item)
    
    def _start_jupyter(self):
        """Start Jupyter Lab server."""
        if self.jupyter_process is not None:
            self.jupyter_log.append("Jupyter Lab is already running!")
            return
        
        try:
            # Start Jupyter Lab
            self.jupyter_process = QProcess()
            self.jupyter_process.setWorkingDirectory(str(self.notebooks_dir))
            
            # Connect signals
            self.jupyter_process.readyReadStandardOutput.connect(self._handle_jupyter_output)
            self.jupyter_process.readyReadStandardError.connect(self._handle_jupyter_error)
            self.jupyter_process.finished.connect(self._jupyter_finished)
            
            # Start process
            jupyter_cmd = "jupyter"
            args = ["lab", "--no-browser", f"--notebook-dir={self.notebooks_dir}"]
            
            self.jupyter_log.append(f"Starting Jupyter Lab in: {self.notebooks_dir}\n")
            self.jupyter_process.start(jupyter_cmd, args)
            
            # Update UI
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status_label.setText("Status: Starting...")
            self.status_label.setStyleSheet("""
                QLabel {
                    padding: 12px;
                    background-color: #F39C12;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: bold;
                    color: #1E1E1E;
                }
            """)
            
            # Wait a bit then open browser
            QTimer.singleShot(3000, self._open_jupyter_browser)
            
        except Exception as e:
            self.jupyter_log.append(f"Error starting Jupyter Lab: {e}\n")
            self._jupyter_finished()
    
    def _stop_jupyter(self):
        """Stop Jupyter Lab server."""
        if self.jupyter_process is not None:
            self.jupyter_log.append("\nStopping Jupyter Lab...\n")
            self.jupyter_process.terminate()
            self.jupyter_process.waitForFinished(3000)
            
            if self.jupyter_process.state() == QProcess.Running:
                self.jupyter_process.kill()
    
    def _handle_jupyter_output(self):
        """Handle Jupyter output."""
        if self.jupyter_process:
            data = bytes(self.jupyter_process.readAllStandardOutput()).decode('utf-8', errors='ignore')
            self.jupyter_log.append(data)
            
            # Extract URL
            if 'http://localhost:' in data or 'http://127.0.0.1:' in data:
                lines = data.split('\n')
                for line in lines:
                    if 'http://' in line and 'token=' in line:
                        # Extract URL
                        start = line.find('http://')
                        if start != -1:
                            url = line[start:].split()[0]
                            self.jupyter_url = url
                            self.status_label.setText(f"Status: Running ✓")
                            self.status_label.setStyleSheet("""
                                QLabel {
                                    padding: 12px;
                                    background-color: #27AE60;
                                    border-radius: 6px;
                                    font-size: 13px;
                                    font-weight: bold;
                                    color: #FFFFFF;
                                }
                            """)
                            break
    
    def _handle_jupyter_error(self):
        """Handle Jupyter errors."""
        if self.jupyter_process:
            data = bytes(self.jupyter_process.readAllStandardError()).decode('utf-8', errors='ignore')
            self.jupyter_log.append(f"<span style='color: #E74C3C;'>{data}</span>")
    
    def _jupyter_finished(self):
        """Handle Jupyter process finished."""
        self.jupyter_process = None
        self.jupyter_url = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Status: Stopped")
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 12px;
                background-color: #E74C3C;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                color: #FFFFFF;
            }
        """)
        self.jupyter_log.append("\nJupyter Lab stopped.\n")
    
    def _open_jupyter_browser(self):
        """Open Jupyter in browser."""
        if self.jupyter_url:
            import webbrowser
            webbrowser.open(self.jupyter_url)
        else:
            # Default URL
            import webbrowser
            webbrowser.open('http://localhost:8888')
    
    def _open_selected_notebook(self):
        """Open selected notebook in Jupyter."""
        current_item = self.notebooks_list.currentItem()
        if current_item:
            notebook_path = current_item.data(Qt.UserRole)
            if notebook_path:
                # Start Jupyter if not running
                if self.jupyter_process is None:
                    self._start_jupyter()
                    # Wait then open specific notebook
                    QTimer.singleShot(4000, lambda: self._open_notebook_url(notebook_path))
                else:
                    self._open_notebook_url(notebook_path)
    
    def _open_notebook_url(self, notebook_path):
        """Open specific notebook URL."""
        import webbrowser
        notebook_name = Path(notebook_path).name
        base_url = self.jupyter_url if self.jupyter_url else 'http://localhost:8888'
        # Remove token from URL and add notebook path
        if '?' in base_url:
            base_url = base_url.split('?')[0]
        notebook_url = f"{base_url}/lab/tree/{notebook_name}"
        webbrowser.open(notebook_url)
    
    def _open_notebooks_folder(self):
        """Open notebooks folder in file explorer."""
        import platform
        import subprocess
        
        if platform.system() == 'Windows':
            os.startfile(self.notebooks_dir)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', self.notebooks_dir])
        else:  # Linux
            subprocess.run(['xdg-open', self.notebooks_dir])
    
    def _open_models_folder(self):
        """Open models folder in file explorer."""
        import platform
        import subprocess
        
        models_dir = Path(__file__).parent.parent.parent / 'models'
        models_dir.mkdir(exist_ok=True)
        
        if platform.system() == 'Windows':
            os.startfile(models_dir)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', models_dir])
        else:  # Linux
            subprocess.run(['xdg-open', models_dir])
    
    def _download_models(self):
        """Run model download script."""
        download_script = Path(__file__).parent.parent.parent / 'download_models.py'
        
        if not download_script.exists():
            QMessageBox.warning(
                None,
                "Script Not Found",
                f"Model download script not found at:\n{download_script}"
            )
            return
        
        # Get Python executable from virtual environment
        venv_python = Path(__file__).parent.parent.parent.parent / '.venv' / 'Scripts' / 'python.exe'
        if not venv_python.exists():
            venv_python = 'python'  # Fallback to system python
        else:
            venv_python = str(venv_python)
        
        # Open in terminal
        import platform
        if platform.system() == 'Windows':
            # Use -NoExit to keep the terminal open after script finishes
            cmd = f'cd "{download_script.parent}"; {venv_python} "{download_script}"; pause'
            subprocess.Popen(['powershell', '-NoExit', '-Command', cmd], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(['python', str(download_script)])
        
        QMessageBox.information(
            None,
            "Model Downloader",
            "Model download script launched in a new terminal window.\n\n"
            "Follow the prompts to download models."
        )
    
    def process(self, data):
        """Process training data."""
        # Can be used for training callbacks
        pass
    
    def cleanup(self):
        """Cleanup when closing."""
        if self.jupyter_process is not None:
            self._stop_jupyter()
        print("Training app cleaned up")


# For standalone testing
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    training_app = TrainingApp()
    training_app.initialize()
    widget = training_app.create_widget()
    widget.show()
    
    sys.exit(app.exec_())
