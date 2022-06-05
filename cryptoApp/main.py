"""Main file for CryptoApp, it's the entry point.
"""
import sys

from PySide6.QtWidgets import QApplication

from utils import new_logger
from crypto_ui import MainWindowCrypto



main_logger = new_logger("MAIN")

main_logger.info("Initialisation of the application...")
app = QApplication(sys.argv)
w = MainWindowCrypto()
w.show()
result = app.exec()

if result == 0:
    main_logger.info("Application interrupted whith success")
else:
    main_logger.warning(f"Application interrupted on a error: {result}")
sys.exit(result)
