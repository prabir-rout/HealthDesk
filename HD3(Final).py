import sys
import subprocess
import google.generativeai as genai

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QHBoxLayout, QTextEdit, QLineEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap

# Configure Gemini API
genai.configure(api_key="#") 

def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text if response.text else "I'm sorry, I couldn't process that."
    except Exception as e:
        return f"Error: {str(e)}"

class HealthAppUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AI-Powered Healthcare App")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon("healthcare.jpg"))

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("HealthDesk")
        title.setFont(QFont("Roboto", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Navigation Buttons
        button_layout = QHBoxLayout()
        self.dashboard_btn = QPushButton("Dashboard")
        self.ai_btn = QPushButton("AI Health Predictor")
        self.reports_btn = QPushButton("Reports")
        self.appointments_btn = QPushButton("Appointments")
        self.settings_btn = QPushButton("Settings")

        for button in [self.dashboard_btn, self.ai_btn, self.reports_btn, self.appointments_btn, self.settings_btn]:
            button.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
            button_layout.addWidget(button)

        # Stacked Widget (to switch between sections)
        self.content_stack = QStackedWidget()
        
        # Dashboard Page
        self.dashboard_page = QWidget()
        dashboard_layout = QVBoxLayout()
        self.user_photo = QLabel()
        self.user_photo.setPixmap(QPixmap("download.jpg").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.user_name = QLabel("Name: CodeOctane")
        self.user_age = QLabel("Age: 20")
        self.user_email = QLabel("Email: CodeOctane@example.com")
        self.user_phone = QLabel("Phone: +1234567890")
        for widget in [self.user_photo, self.user_name, self.user_age, self.user_email, self.user_phone]:
            widget.setFont(QFont("Roboto", 14))
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dashboard_layout.addWidget(widget)
        self.dashboard_page.setLayout(dashboard_layout)

        # Appointments Page
        self.appointments_page = QWidget()
        appointments_layout = QVBoxLayout()
        doctor_list = [
            ("Dr. Smith - Cardiologist", "+1234567891"),
            ("Dr. Johnson - Neurologist", "+1234567892"),
            ("Dr. Brown - Dermatologist", "+1234567893"),
        ]
        for name, contact in doctor_list:
            doc_label = QLabel(f"{name} - {contact}")
            doc_label.setFont(QFont("Roboto", 14))
            appointments_layout.addWidget(doc_label)
        self.book_appointment_btn = QPushButton("Book Appointment")
        self.book_appointment_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 10px; font-size: 14px; border-radius: 5px;")
        appointments_layout.addWidget(self.book_appointment_btn)
        self.appointments_page.setLayout(appointments_layout)

        # AI Health Predictor Page
        self.ai_page = QWidget()
        ai_layout = QVBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your health query...")
        self.send_button = QPushButton("Ask AI")
        self.send_button.clicked.connect(self.run_gemini)
        ai_layout.addWidget(self.user_input)
        ai_layout.addWidget(self.send_button)
        self.ai_page.setLayout(ai_layout)

        # Reports Page
        self.reports_page = QWidget()
        reports_layout = QVBoxLayout()
        self.reports_text = QTextEdit()
        self.reports_text.setReadOnly(True)
        reports_layout.addWidget(self.reports_text)
        self.reports_page.setLayout(reports_layout)

        # Settings Page
        self.settings_page = QLabel("Modify your app settings here.", alignment=Qt.AlignmentFlag.AlignCenter)
        self.settings_page.setFont(QFont("Roboto", 16))

        # Add pages to content stack
        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.ai_page)
        self.content_stack.addWidget(self.reports_page)
        self.content_stack.addWidget(self.appointments_page)
        self.content_stack.addWidget(self.settings_page)

        # Connect buttons to switch pages
        self.dashboard_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.dashboard_page))
        self.ai_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.ai_page))
        self.reports_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.reports_page))
        self.appointments_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.appointments_page))
        self.settings_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.settings_page))

        # Add elements to main layout
        main_layout.addWidget(title)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.content_stack)
        main_widget.setLayout(main_layout)

    def run_gemini(self):
        """Fetch AI response from Gemini API and store in reports page."""
        user_input = self.user_input.text().strip()
        if not user_input:
            return

        self.reports_text.append(f"User: {user_input}")
        self.user_input.clear()

        # Simulate AI typing delay
        QTimer.singleShot(2000, lambda: self.get_gemini_response(user_input))
    
    def get_gemini_response(self, user_input):
        ai_response = get_gemini_response(user_input)
        self.reports_text.append(f"AI: {ai_response}")
        self.reports_text.append("\n----------------------\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HealthAppUI()
    window.show()
    sys.exit(app.exec())
