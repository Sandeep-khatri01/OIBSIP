from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont

class ResultWidget(QWidget):
    """Widget to display BMI calculation results with visual feedback"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Your BMI Result")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setObjectName("resultTitle")
        layout.addWidget(title)
        
        # BMI Value Display (Large)
        self.bmi_label = QLabel("--")
        self.bmi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bmi_label.setFont(QFont("Segoe UI", 48, QFont.Weight.Bold))
        self.bmi_label.setObjectName("bmiValue")
        layout.addWidget(self.bmi_label)
        
        # Category Label
        self.category_label = QLabel("Enter your details to calculate")
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.category_label.setFont(QFont("Segoe UI", 16))
        self.category_label.setObjectName("categoryLabel")
        layout.addWidget(self.category_label)
        
        # BMI Scale Reference
        scale_frame = QFrame()
        scale_frame.setObjectName("scaleFrame")
        scale_layout = QVBoxLayout(scale_frame)
        scale_layout.setSpacing(8)
        
        scale_title = QLabel("BMI Categories:")
        scale_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        scale_layout.addWidget(scale_title)
        
        categories = [
            ("< 18.5", "Underweight", "#64B5F6"),
            ("18.5 - 24.9", "Normal", "#66BB6A"),
            ("25.0 - 29.9", "Overweight", "#FFA726"),
            ("≥ 30.0", "Obese", "#EF5350")
        ]
        
        for range_text, category, color in categories:
            cat_label = QLabel(f"  {range_text} - {category}")
            cat_label.setStyleSheet(f"color: {color}; font-weight: bold;")
            scale_layout.addWidget(cat_label)
        
        layout.addWidget(scale_frame)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setObjectName("resultWidget")
    
    def update_result(self, bmi, category):
        """Update the displayed BMI result with color coding"""
        self.bmi_label.setText(f"{bmi:.1f}")
        self.category_label.setText(category)
        
        # Color code based on category
        color_map = {
            "Underweight": "#64B5F6",
            "Normal weight": "#66BB6A",
            "Overweight": "#FFA726",
            "Obese": "#EF5350"
        }
        
        color = color_map.get(category, "#FFFFFF")
        self.bmi_label.setStyleSheet(f"color: {color};")
        self.category_label.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def clear_result(self):
        """Clear the result display"""
        self.bmi_label.setText("--")
        self.category_label.setText("Enter your details to calculate")
        self.bmi_label.setStyleSheet("")
        self.category_label.setStyleSheet("")
