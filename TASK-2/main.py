import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from bmi_calculator.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Load light theme stylesheet by default
    try:
        with open(os.path.join(os.path.dirname(__file__), "styles_light.qss"), "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: styles_light.qss not found")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
