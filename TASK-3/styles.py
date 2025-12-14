MINIMALIST_THEME = """
QMainWindow {
    background-color: #f8f9fa;
}

QFrame#Card {
    background-color: #ffffff;
    border: none;
    border-radius: 16px;
    padding: 10px;
}

QLabel {
    color: #2c3e50;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
    background: transparent;
}

QLabel#Title {
    font-size: 32px;
    font-weight: 300;
    color: #1a1a1a;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
}

QLabel#PasswordDisplay {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    color: #2c3e50;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 18px;
    font-weight: 500;
    padding: 18px;
    selection-background-color: #d4e3fc;
}

QPushButton {
    background-color: #4a90e2;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 500;
    font-size: 14px;
    letter-spacing: 0.3px;
}

QPushButton:hover {
    background-color: #357abd;
}

QPushButton:pressed {
    background-color: #2868a8;
}

QPushButton#CopyButton {
    background-color: #f8f9fa;
    color: #4a90e2;
    border: 1px solid #e9ecef;
}

QPushButton#CopyButton:hover {
    background-color: #e9ecef;
    border-color: #4a90e2;
}

QPushButton#ThemeToggle {
    background-color: transparent;
    color: #6c757d;
    border: 1px solid #dee2e6;
    padding: 8px 16px;
    font-size: 12px;
}

QPushButton#ThemeToggle:hover {
    background-color: #f8f9fa;
    border-color: #4a90e2;
    color: #4a90e2;
}

QPushButton#ClearHistoryButton {
    background-color: transparent;
    color: #dc3545;
    border: 1px solid #dee2e6;
    padding: 6px 12px;
    font-size: 12px;
}

QPushButton#ClearHistoryButton:hover {
    background-color: #dc3545;
    color: #ffffff;
    border-color: #dc3545;
}

QCheckBox {
    color: #495057;
    font-size: 13px;
    spacing: 12px;
    background: transparent;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #dee2e6;
    background-color: #ffffff;
}

QCheckBox::indicator:hover {
    border-color: #4a90e2;
}

QCheckBox::indicator:checked {
    background-color: #4a90e2;
    border-color: #4a90e2;
}

QSlider::groove:horizontal {
    border: none;
    height: 4px;
    background: #e9ecef;
    margin: 2px 0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #4a90e2;
    border: none;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #357abd;
}

QSpinBox {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 6px;
    color: #2c3e50;
    padding: 8px;
    font-size: 13px;
    min-width: 60px;
}

QSpinBox:focus {
    border-color: #4a90e2;
}

QLineEdit {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 6px;
    color: #2c3e50;
    padding: 8px;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #4a90e2;
}

QListWidget {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    color: #2c3e50;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    padding: 5px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 4px;
}

QListWidget::item:hover {
    background-color: #e9ecef;
}

QListWidget::item:selected {
    background-color: #d4e3fc;
    color: #2c3e50;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: #1a1a1a;
}

QFrame#Card {
    background-color: #2d2d2d;
    border: none;
    border-radius: 16px;
    padding: 10px;
}

QLabel {
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
    background: transparent;
}

QLabel#Title {
    font-size: 32px;
    font-weight: 300;
    color: #ffffff;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
}

QLabel#PasswordDisplay {
    background-color: #1f1f1f;
    border: 1px solid #404040;
    border-radius: 10px;
    color: #e0e0e0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 18px;
    font-weight: 500;
    padding: 18px;
    selection-background-color: #4a5568;
}

QPushButton {
    background-color: #4a90e2;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 500;
    font-size: 14px;
    letter-spacing: 0.3px;
}

QPushButton:hover {
    background-color: #357abd;
}

QPushButton:pressed {
    background-color: #2868a8;
}

QPushButton#CopyButton {
    background-color: #1f1f1f;
    color: #4a90e2;
    border: 1px solid #404040;
}

QPushButton#CopyButton:hover {
    background-color: #404040;
    border-color: #4a90e2;
}

QPushButton#ThemeToggle {
    background-color: transparent;
    color: #a0a0a0;
    border: 1px solid #404040;
    padding: 8px 16px;
    font-size: 12px;
}

QPushButton#ThemeToggle:hover {
    background-color: #1f1f1f;
    border-color: #4a90e2;
    color: #4a90e2;
}

QPushButton#ClearHistoryButton {
    background-color: transparent;
    color: #ff6b6b;
    border: 1px solid #404040;
    padding: 6px 12px;
    font-size: 12px;
}

QPushButton#ClearHistoryButton:hover {
    background-color: #ff6b6b;
    color: #ffffff;
    border-color: #ff6b6b;
}

QCheckBox {
    color: #b0b0b0;
    font-size: 13px;
    spacing: 12px;
    background: transparent;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #404040;
    background-color: #2d2d2d;
}

QCheckBox::indicator:hover {
    border-color: #4a90e2;
}

QCheckBox::indicator:checked {
    background-color: #4a90e2;
    border-color: #4a90e2;
}

QSlider::groove:horizontal {
    border: none;
    height: 4px;
    background: #404040;
    margin: 2px 0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #4a90e2;
    border: none;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #357abd;
}

QSpinBox {
    background-color: #1f1f1f;
    border: 1px solid #404040;
    border-radius: 6px;
    color: #e0e0e0;
    padding: 8px;
    font-size: 13px;
    min-width: 60px;
}

QSpinBox:focus {
    border-color: #4a90e2;
}

QLineEdit {
    background-color: #1f1f1f;
    border: 1px solid #404040;
    border-radius: 6px;
    color: #e0e0e0;
    padding: 8px;
    font-size: 13px;
}

QLineEdit:focus {
    border-color: #4a90e2;
}

QListWidget {
    background-color: #1f1f1f;
    border: 1px solid #404040;
    border-radius: 8px;
    color: #e0e0e0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    padding: 5px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 4px;
}

QListWidget::item:hover {
    background-color: #404040;
}

QListWidget::item:selected {
    background-color: #4a5568;
    color: #e0e0e0;
}
"""

