from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QMessageBox, QFormLayout
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPainter, QPixmap, QFont
import os

class InputWidget(QWidget):
    calculate_signal = pyqtSignal(float, float) # weight, height
    user_changed_signal = pyqtSignal(int) # user_id
    add_user_signal = pyqtSignal(str) # username

    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("BMI Calculator")
        title.setObjectName("inputTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        from PyQt6.QtGui import QFont
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        # User Selection Section
        user_section = QWidget()
        user_section.setObjectName("userSection")
        user_layout = QVBoxLayout(user_section)
        user_layout.setSpacing(10)
        
        user_label = QLabel("Select User:")
        user_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        user_layout.addWidget(user_label)
        
        user_controls = QHBoxLayout()
        self.user_combo = QComboBox()
        self.user_combo.setMinimumHeight(40)
        self.user_combo.currentIndexChanged.connect(self.on_user_changed)
        self.add_user_btn = QPushButton("➕ Add User")
        self.add_user_btn.clicked.connect(self.add_user)
        self.add_user_btn.setMinimumHeight(40)
        user_controls.addWidget(self.user_combo, 3)
        user_controls.addWidget(self.add_user_btn, 1)
        user_layout.addLayout(user_controls)
        
        layout.addWidget(user_section)

        # Input Form Section
        form_section = QWidget()
        form_section.setObjectName("formSection")
        form_layout = QVBoxLayout(form_section)
        form_layout.setSpacing(15)
        
        # Weight Input
        weight_label = QLabel("Weight (kg):")
        weight_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        form_layout.addWidget(weight_label)
        
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter weight in kilograms (e.g., 70)")
        self.weight_input.setMinimumHeight(45)
        self.weight_input.setFont(QFont("Segoe UI", 12))
        form_layout.addWidget(self.weight_input)
        
        # Height Input
        height_label = QLabel("Height (m):")
        height_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        form_layout.addWidget(height_label)
        
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter height in meters (e.g., 1.75)")
        self.height_input.setMinimumHeight(45)
        self.height_input.setFont(QFont("Segoe UI", 12))
        form_layout.addWidget(self.height_input)
        
        layout.addWidget(form_section)

        # Calculate Button
        self.calc_btn = QPushButton("Calculate BMI")
        self.calc_btn.clicked.connect(self.calculate)
        self.calc_btn.setMinimumHeight(50)
        self.calc_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.calc_btn.setObjectName("calculateButton")
        layout.addWidget(self.calc_btn)
        
        layout.addStretch()

        self.setLayout(layout)
        self.refresh_users()

    def refresh_users(self):
        self.user_combo.blockSignals(True)
        self.user_combo.clear()
        
        # Add placeholder item
        self.user_combo.addItem("-- Select or Add a User --", None)
        
        # Add existing users
        users = self.db_manager.get_users()
        for user_id, name in users:
            self.user_combo.addItem(name, user_id)
        
        self.user_combo.blockSignals(False)
        
        # Don't auto-select any user, keep placeholder selected
        self.user_combo.setCurrentIndex(0)

    def add_user(self):
        # In a real app, use QInputDialog, but for simplicity we can use a separate dialog or just a simple input here.
        # For now, let's assume we want to trigger a dialog in the main window or handle it here.
        # Let's use a simple input dialog here for ease.
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Add User", "Enter user name:")
        if ok and name:
            self.add_user_signal.emit(name)

    def on_user_changed(self):
        user_id = self.user_combo.currentData()
        if user_id is not None:
            self.user_changed_signal.emit(user_id)
        else:
            # Placeholder selected, clear history
            # Emit signal to clear history display
            pass

    def calculate(self):
        try:
            weight = float(self.weight_input.text())
            height = float(self.height_input.text())
            self.calculate_signal.emit(weight, height)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for weight and height.")
