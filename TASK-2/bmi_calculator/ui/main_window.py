from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from .input_widget import InputWidget
from .history_widget import HistoryWidget
from ..database import DatabaseManager
from ..logic import BMILogic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BMI Calculator")
        self.setGeometry(100, 100, 900, 700)

        self.db_manager = DatabaseManager()
        self.is_dark_mode = False  # Start with light mode
        
        self.init_ui()
        self.apply_theme()  # Apply initial theme

    def init_ui(self):
        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top bar with dark mode toggle
        from PyQt6.QtWidgets import QPushButton
        from PyQt6.QtCore import Qt
        top_bar = QWidget()
        top_bar.setObjectName("topBar")
        top_bar.setMaximumHeight(50)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(15, 5, 15, 5)
        
        top_bar_layout.addStretch()
        
        self.theme_toggle_btn = QPushButton("🌙 Dark Mode")
        self.theme_toggle_btn.setObjectName("themeToggle")
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self.theme_toggle_btn.setMinimumWidth(120)
        self.theme_toggle_btn.setMinimumHeight(35)
        top_bar_layout.addWidget(self.theme_toggle_btn)
        
        main_layout.addWidget(top_bar)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Calculator Tab with horizontal layout
        calc_tab = QWidget()
        calc_layout = QHBoxLayout(calc_tab)
        calc_layout.setSpacing(0)
        calc_layout.setContentsMargins(0, 0, 0, 0)
        
        # Input Widget (left side)
        self.input_widget = InputWidget(self.db_manager)
        self.input_widget.calculate_signal.connect(self.calculate_bmi)
        self.input_widget.user_changed_signal.connect(self.load_history)
        self.input_widget.add_user_signal.connect(self.add_user)
        calc_layout.addWidget(self.input_widget, 1)
        
        # Result Widget (right side)
        from .result_widget import ResultWidget
        self.result_widget = ResultWidget()
        calc_layout.addWidget(self.result_widget, 1)
        
        self.tabs.addTab(calc_tab, "Calculator")

        # History Tab
        self.history_widget = HistoryWidget()
        self.history_widget.clear_btn.clicked.connect(self.clear_history)
        self.tabs.addTab(self.history_widget, "History & Trends")
        
        # Don't auto-load any user on startup - let user select manually

    def add_user(self, name):
        user_id = self.db_manager.add_user(name)
        if user_id:
            QMessageBox.information(self, "Success", f"User '{name}' added successfully!")
            self.input_widget.refresh_users()
        else:
            QMessageBox.warning(self, "Error", f"User '{name}' already exists!")

    def calculate_bmi(self, weight, height):
        try:
            bmi = BMILogic.calculate_bmi(weight, height)
            category = BMILogic.get_category(bmi)
            
            user_id = self.input_widget.user_combo.currentData()
            if user_id is None:
                QMessageBox.warning(self, "Error", "Please select or add a user first.")
                return

            # Save record
            self.db_manager.add_record(user_id, weight, height, bmi)
            
            # Show result in result widget
            self.result_widget.update_result(bmi, category)
            
            # Refresh history
            self.load_history(user_id)
            
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def load_history(self, user_id):
        records = self.db_manager.get_records(user_id)
        self.history_widget.update_data(records)

    def clear_history(self):
        user_id = self.input_widget.user_combo.currentData()
        if user_id is None:
            return

        reply = QMessageBox.question(
            self, 'Confirm Delete', 
            "Are you sure you want to clear all history for this user?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_records(user_id)
            self.load_history(user_id)
            QMessageBox.information(self, "Success", "History cleared successfully.")
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to the application"""
        import os
        
        if self.is_dark_mode:
            theme_file = "styles_dark.qss"
            self.theme_toggle_btn.setText("☀️ Light Mode")
        else:
            theme_file = "styles_light.qss"
            self.theme_toggle_btn.setText("🌙 Dark Mode")
        
        # Load and apply stylesheet
        theme_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), theme_file)
        try:
            with open(theme_path, "r") as f:
                self.parent().setStyleSheet(f.read()) if self.parent() else None
                # Apply to QApplication instead
                from PyQt6.QtWidgets import QApplication
                QApplication.instance().setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: {theme_file} not found")
