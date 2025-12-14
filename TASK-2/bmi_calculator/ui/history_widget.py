from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtGui import QPainter, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import datetime
import os

class HistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        from PyQt6.QtGui import QFont
        from PyQt6.QtCore import Qt
        title = QLabel("BMI History & Trends")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setObjectName("inputTitle")
        layout.addWidget(title)
        
        # Summary Statistics Panel
        from PyQt6.QtWidgets import QHBoxLayout, QFrame
        stats_frame = QFrame()
        stats_frame.setObjectName("scaleFrame")
        stats_layout = QHBoxLayout(stats_frame)
        
        self.avg_label = QLabel("Avg BMI: --")
        self.avg_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.avg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.min_label = QLabel("Min BMI: --")
        self.min_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.max_label = QLabel("Max BMI: --")
        self.max_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.count_label = QLabel("Records: 0")
        self.count_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        stats_layout.addWidget(self.avg_label)
        stats_layout.addWidget(self.min_label)
        stats_layout.addWidget(self.max_label)
        stats_layout.addWidget(self.count_label)
        
        layout.addWidget(stats_frame)

        # Graph
        self.figure = Figure(figsize=(8, 4))
        self.figure.patch.set_alpha(0.0)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: transparent;")
        self.canvas.setMinimumHeight(300)
        layout.addWidget(self.canvas)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Weight (kg)", "Height (m)", "BMI"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(200)
        layout.addWidget(self.table)

        # Clear Data Button
        from PyQt6.QtWidgets import QPushButton
        self.clear_btn = QPushButton("🗑️ Clear History")
        self.clear_btn.setObjectName("clearButton")
        self.clear_btn.setMinimumHeight(45)
        self.clear_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(self.clear_btn)

        self.setLayout(layout)

    def update_data(self, records):
        # Update statistics
        if records:
            bmis = [bmi for _, _, bmi, _ in records]
            avg_bmi = sum(bmis) / len(bmis)
            min_bmi = min(bmis)
            max_bmi = max(bmis)
            
            self.avg_label.setText(f"Avg BMI: {avg_bmi:.1f}")
            self.min_label.setText(f"Min BMI: {min_bmi:.1f}")
            self.max_label.setText(f"Max BMI: {max_bmi:.1f}")
            self.count_label.setText(f"Records: {len(records)}")
        else:
            self.avg_label.setText("Avg BMI: --")
            self.min_label.setText("Min BMI: --")
            self.max_label.setText("Max BMI: --")
            self.count_label.setText("Records: 0")
        
        # Update Table
        self.table.setRowCount(len(records))
        dates = []
        bmis = []

        for i, (weight, height, bmi, date_str) in enumerate(records):
            # Parse date
            try:
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                date_obj = datetime.datetime.now()

            self.table.setItem(i, 0, QTableWidgetItem(date_str))
            self.table.setItem(i, 1, QTableWidgetItem(f"{weight:.1f}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{height:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{bmi:.1f}"))
            
            dates.append(date_obj)
            bmis.append(bmi)

        # Update Graph
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        self.figure.patch.set_facecolor('none')
        ax.set_facecolor((0.96, 0.96, 0.96, 0.5))  # Light gray with transparency

        if dates:
            # Plot with styled line and markers
            line, = ax.plot(dates, bmis, marker='o', linestyle='-', linewidth=2.5, markersize=8)
            line.set_color('#1976D2')  # Blue
            line.set_markerfacecolor('#1976D2')
            line.set_markeredgecolor('#0D47A1')
            line.set_markeredgewidth(2)
            
            ax.set_title("BMI Trend Over Time", color='#212121', fontsize=14, fontweight='bold', pad=15)
            ax.set_xlabel("Date", color='#616161', fontsize=11)
            ax.set_ylabel("BMI", color='#616161', fontsize=11)
            
            # Style ticks
            ax.tick_params(axis='x', colors='#616161', labelsize=9)
            ax.tick_params(axis='y', colors='#616161', labelsize=9)
            
            # Style spines
            for spine in ax.spines.values():
                spine.set_color('#BDBDBD')
                spine.set_linewidth(1)

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            self.figure.autofmt_xdate()
            ax.grid(True, color='#E0E0E0', linestyle='--', alpha=0.7)
        
        self.canvas.draw()
