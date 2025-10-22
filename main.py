"""
TensorRT Model Converter Application
Main entry point for the application.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.main_window import run_gui
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main entry point for the application."""
    logger.info("Starting TensorRT Model Converter Application")
    
    try:
        run_gui()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
