import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QCheckBox, QSlider, QSpinBox, 
    QFrame, QApplication, QLineEdit, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard, QIcon
import pyperclip
from generator import PasswordGenerator
from styles import MINIMALIST_THEME, DARK_THEME

class PasswordGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.generator = PasswordGenerator()
        self.dark_mode = False
        self.password_history = []  # Store copied passwords
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Generator")
        self.setGeometry(100, 100, 600, 850)
        self.setStyleSheet(MINIMALIST_THEME)

        # Main Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Card Frame
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(500)
        main_layout.addWidget(card)

        # Card Layout
        layout = QVBoxLayout(card)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title and Theme Toggle
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        title_label = QLabel("Password Generator")
        title_label.setObjectName("Title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.theme_toggle_btn = QPushButton("🌙 Dark")
        self.theme_toggle_btn.setObjectName("ThemeToggle")
        self.theme_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self.theme_toggle_btn.setToolTip("Toggle dark mode")
        self.theme_toggle_btn.setFixedWidth(100)
        
        title_layout.addStretch()
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.theme_toggle_btn)
        
        layout.addLayout(title_layout)

        # Password Display
        self.password_display = QLabel("Click Generate")
        self.password_display.setObjectName("PasswordDisplay")
        self.password_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_display.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.password_display.setToolTip("Your generated password will appear here")
        layout.addWidget(self.password_display)

        # Strength Indicator
        self.strength_label = QLabel("Strength: N/A")
        self.strength_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.strength_label)

        # Controls Container
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(15)
        layout.addLayout(controls_layout)

        # Length Control
        length_layout = QHBoxLayout()
        length_label = QLabel("Length:")
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(4, 64)
        self.length_slider.setValue(12)
        self.length_slider.setToolTip("Slide to adjust password length")
        
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(4, 64)
        self.length_spinbox.setValue(12)
        self.length_spinbox.setToolTip("Enter exact password length")

        # Connect slider and spinbox
        self.length_slider.valueChanged.connect(self.length_spinbox.setValue)
        self.length_spinbox.valueChanged.connect(self.length_slider.setValue)

        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_slider)
        length_layout.addWidget(self.length_spinbox)
        controls_layout.addLayout(length_layout)

        # Options
        self.check_upper = QCheckBox("Uppercase (A-Z)")
        self.check_upper.setChecked(True)
        self.check_upper.setToolTip("Include uppercase letters")
        
        self.check_lower = QCheckBox("Lowercase (a-z)")
        self.check_lower.setChecked(True)
        self.check_lower.setToolTip("Include lowercase letters")
        
        self.check_digits = QCheckBox("Numbers (0-9)")
        self.check_digits.setChecked(True)
        self.check_digits.setToolTip("Include numbers")
        
        self.check_symbols = QCheckBox("Symbols (!@#$)")
        self.check_symbols.setChecked(True)
        self.check_symbols.setToolTip("Include special characters")

        controls_layout.addWidget(self.check_upper)
        controls_layout.addWidget(self.check_lower)
        controls_layout.addWidget(self.check_digits)
        controls_layout.addWidget(self.check_symbols)

        # Exclusion Input
        exclusion_layout = QHBoxLayout()
        exclusion_label = QLabel("Exclude Characters:")
        self.exclusion_input = QLineEdit()
        self.exclusion_input.setPlaceholderText("e.g. l1O0")
        self.exclusion_input.setToolTip("Enter characters you want to exclude from the password")
        
        exclusion_layout.addWidget(exclusion_label)
        exclusion_layout.addWidget(self.exclusion_input)
        controls_layout.addLayout(exclusion_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.generate_btn = QPushButton("Generate Password")
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_btn.clicked.connect(self.generate_password)
        self.generate_btn.setToolTip("Generate a new password based on settings")
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.setObjectName("CopyButton")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setToolTip("Copy the current password to clipboard")

        buttons_layout.addWidget(self.generate_btn)
        buttons_layout.addWidget(self.copy_btn)
        
        layout.addLayout(buttons_layout)
        
        # Password History Section
        history_header_layout = QHBoxLayout()
        history_header_layout.setSpacing(10)
        
        history_label = QLabel("Recent Copied Passwords")
        history_label.setObjectName("HistoryLabel")
        history_label.setStyleSheet("font-size: 14px; font-weight: 500; margin-top: 10px;")
        
        self.clear_history_btn = QPushButton("Clear")
        self.clear_history_btn.setObjectName("ClearHistoryButton")
        self.clear_history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_history_btn.clicked.connect(self.clear_history)
        self.clear_history_btn.setToolTip("Clear password history")
        self.clear_history_btn.setFixedWidth(80)
        
        history_header_layout.addWidget(history_label)
        history_header_layout.addStretch()
        history_header_layout.addWidget(self.clear_history_btn)
        
        layout.addLayout(history_header_layout)
        
        # History List
        self.history_list = QListWidget()
        self.history_list.setObjectName("HistoryList")
        self.history_list.setMaximumHeight(150)
        self.history_list.setToolTip("Click on a password to copy it again")
        self.history_list.itemClicked.connect(self.copy_from_history)
        layout.addWidget(self.history_list)
        # Removed addStretch since we want the card to be compact
        
        # Initial Generation
        self.generate_password()

    def generate_password(self):
        length = self.length_spinbox.value()
        use_upper = self.check_upper.isChecked()
        use_lower = self.check_lower.isChecked()
        use_digits = self.check_digits.isChecked()
        use_symbols = self.check_symbols.isChecked()
        exclude_chars = self.exclusion_input.text()

        password = self.generator.generate(length, use_upper, use_lower, use_digits, use_symbols, exclude_chars)
        self.password_display.setText(password)

        # Update Strength
        if "Error" not in password:
            strength, color = self.generator.check_strength(password)
            self.strength_label.setText(f"Strength: {strength}")
            self.strength_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        else:
            self.strength_label.setText("Error")
            self.strength_label.setStyleSheet("color: #ff4d4d; font-weight: bold;")

    def copy_to_clipboard(self):
        password = self.password_display.text()
        if "Error" not in password and password != "Click Generate":
            pyperclip.copy(password)
            
            # Add to history
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"{password} ({timestamp})"
            
            # Avoid duplicates
            if password not in [entry.split(" (")[0] for entry in self.password_history]:
                self.password_history.insert(0, history_entry)
                # Keep only last 10
                if len(self.password_history) > 10:
                    self.password_history.pop()
                self.update_history_display()
            
            original_text = self.copy_btn.text()
            self.copy_btn.setText("Copied!")
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, lambda: self.copy_btn.setText("Copy to Clipboard"))

    def update_history_display(self):
        self.history_list.clear()
        for entry in self.password_history:
            item = QListWidgetItem(entry)
            item.setToolTip("Click to copy this password")
            self.history_list.addItem(item)
    
    def copy_from_history(self, item):
        # Extract password from "password (timestamp)" format
        password = item.text().split(" (")[0]
        pyperclip.copy(password)
        self.copy_btn.setText("Copied!")
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.copy_btn.setText("Copy to Clipboard"))
    
    def clear_history(self):
        self.password_history.clear()
        self.history_list.clear()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet(DARK_THEME)
            self.theme_toggle_btn.setText("☀️ Light")
        else:
            self.setStyleSheet(MINIMALIST_THEME)
            self.theme_toggle_btn.setText("🌙 Dark")
