# discount_code_app.py

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, 
                             QVBoxLayout, QWidget, QCheckBox, QMessageBox, QSpinBox, QFormLayout, QScrollArea)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from discount_codes import generate_code, verify_code, mark_code_as_used
from datetime import datetime

class DiscountApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Discount Code Application')
        self.setGeometry(100, 100, 800, 600)  # Increased size for better usability
        self.setStyleSheet("background-color: #333; color: #ddd;")  # Dark theme

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #333;")

        # Scrollable content widget
        self.scroll_content_widget = QWidget()
        self.scroll_content_layout = QVBoxLayout()
        self.scroll_content_widget.setLayout(self.scroll_content_layout)
        self.scroll_area.setWidget(self.scroll_content_widget)

        # Add scroll area to main layout
        self.main_layout.addWidget(self.scroll_area)

        # Header
        self.header_label = QLabel('Discount Code Application', self)
        self.header_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("color: #ddd; padding: 15px;")
        self.scroll_content_layout.addWidget(self.header_label)

        # Sections
        self.init_generate_code_section()
        self.init_verify_code_section()
        self.init_apply_code_section()

        # Timer for live countdown
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second

    def init_generate_code_section(self):
        self.label_generate = QLabel('Enter discount amount (NRs):', self)
        self.label_generate.setFont(QFont("Arial", 14))
        self.label_generate.setStyleSheet("color: #ddd; padding: 10px;")
        
        self.amount_input = QLineEdit(self)
        self.amount_input.setFont(QFont("Arial", 12))
        self.amount_input.setStyleSheet(self.input_style())
        
        self.duration_form = QFormLayout()

        self.months_spinbox = QSpinBox(self)
        self.months_spinbox.setMinimum(0)
        self.months_spinbox.setMaximum(12)
        self.months_spinbox.setPrefix('Months: ')
        self.duration_form.addRow(self.months_spinbox)

        self.days_spinbox = QSpinBox(self)
        self.days_spinbox.setMinimum(0)
        self.days_spinbox.setMaximum(31)
        self.days_spinbox.setPrefix('Days: ')
        self.duration_form.addRow(self.days_spinbox)

        self.hours_spinbox = QSpinBox(self)
        self.hours_spinbox.setMinimum(0)
        self.hours_spinbox.setMaximum(23)
        self.hours_spinbox.setPrefix('Hours: ')
        self.duration_form.addRow(self.hours_spinbox)

        self.minutes_spinbox = QSpinBox(self)
        self.minutes_spinbox.setMinimum(0)
        self.minutes_spinbox.setMaximum(59)
        self.minutes_spinbox.setPrefix('Minutes: ')
        self.duration_form.addRow(self.minutes_spinbox)

        self.seconds_spinbox = QSpinBox(self)
        self.seconds_spinbox.setMinimum(0)
        self.seconds_spinbox.setMaximum(59)
        self.seconds_spinbox.setPrefix('Seconds: ')
        self.duration_form.addRow(self.seconds_spinbox)

        self.generate_button = QPushButton('Generate Code', self)
        self.generate_button.setFont(QFont("Arial", 12))
        self.generate_button.setStyleSheet(self.button_style())
        
        self.generated_code_label = QLabel('', self)
        self.generated_code_label.setFont(QFont("Arial", 12))
        self.generated_code_label.setStyleSheet("padding: 15px; background-color: #555; border-radius: 10px;")

        self.scroll_content_layout.addWidget(self.label_generate)
        self.scroll_content_layout.addWidget(self.amount_input)
        self.scroll_content_layout.addLayout(self.duration_form)
        self.scroll_content_layout.addWidget(self.generate_button)
        self.scroll_content_layout.addWidget(self.generated_code_label)

        self.generate_button.clicked.connect(self.generate_code)

    def init_verify_code_section(self):
        self.label_verify = QLabel('Enter discount code to verify:', self)
        self.label_verify.setFont(QFont("Arial", 14))
        self.label_verify.setStyleSheet("color: #ddd; padding: 10px;")
        
        self.code_input = QLineEdit(self)
        self.code_input.setFont(QFont("Arial", 12))
        self.code_input.setStyleSheet(self.input_style())
        
        self.verify_button = QPushButton('Verify Code', self)
        self.verify_button.setFont(QFont("Arial", 12))
        self.verify_button.setStyleSheet(self.button_style())
        
        self.result_label = QLabel('', self)
        self.result_label.setFont(QFont("Arial", 12))
        self.result_label.setStyleSheet("padding: 15px; background-color: #555; border-radius: 10px;")

        self.scroll_content_layout.addWidget(self.label_verify)
        self.scroll_content_layout.addWidget(self.code_input)
        self.scroll_content_layout.addWidget(self.verify_button)
        self.scroll_content_layout.addWidget(self.result_label)

        self.verify_button.clicked.connect(self.verify_code)

    def init_apply_code_section(self):
        self.use_checkbox = QCheckBox('Mark code as used', self)
        self.use_checkbox.setFont(QFont("Arial", 12))
        self.use_checkbox.setStyleSheet("padding: 10px;")
        
        self.mark_button = QPushButton('Apply Code', self)
        self.mark_button.setFont(QFont("Arial", 12))
        self.mark_button.setStyleSheet(self.button_style())
        
        self.scroll_content_layout.addWidget(self.use_checkbox)
        self.scroll_content_layout.addWidget(self.mark_button)

        self.mark_button.clicked.connect(self.confirm_apply_code)

    def generate_code(self):
        try:
            amount = int(self.amount_input.text().strip())
            months = self.months_spinbox.value()
            days = self.days_spinbox.value()
            hours = self.hours_spinbox.value()
            minutes = self.minutes_spinbox.value()
            seconds = self.seconds_spinbox.value()

            if amount <= 0:
                self.generated_code_label.setText('Invalid amount. Enter a positive number.')
            else:
                duration = {'months': months, 'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds}
                code = generate_code(amount, duration)
                self.generated_code_label.setText(f'Generated Code: {code}')
        except ValueError:
            self.generated_code_label.setText('Please enter a valid number.')

    def verify_code(self):
        code = self.code_input.text().strip()
        result = verify_code(code)
        if result:
            expiration = datetime.strptime(result['expiration'], "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            remaining_time = expiration - now
            if result['used']:
                QMessageBox.warning(self, 'Expired Code', 'Code has already been used.')
                self.result_label.setText('')
            elif remaining_time.total_seconds() <= 0:
                QMessageBox.warning(self, 'Expired Code', 'Code has expired.')
                self.result_label.setText('')
            else:
                hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                self.result_label.setText(f'Code is valid. Expires on {expiration}. Time left: {int(hours)}h {int(minutes)}m {int(seconds)}s')
        else:
            QMessageBox.warning(self, 'Invalid Code', 'Invalid code.')

    def confirm_apply_code(self):
        code = self.code_input.text().strip()
        result = verify_code(code)
        if result:
            expiration = datetime.strptime(result['expiration'], "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            if result['used']:
                QMessageBox.warning(self, 'Expired Code', 'Code has already been used.')
            elif expiration < now:
                QMessageBox.warning(self, 'Expired Code', 'Code has expired and cannot be used.')
            else:
                if self.use_checkbox.isChecked():
                    if mark_code_as_used(code):
                        QMessageBox.information(self, 'Success', 'Code marked as used successfully!')
                    else:
                        QMessageBox.warning(self, 'Error', 'Failed to mark the code as used or the code does not exist.')
                else:
                    QMessageBox.warning(self, 'Info', 'You need to check the "Mark code as used" checkbox to apply the code.')
        else:
            QMessageBox.warning(self, 'Invalid Code', 'Invalid code.')

    def update_timer(self):
        code = self.code_input.text().strip()
        if code:
            result = verify_code(code)
            if result:
                expiration = datetime.strptime(result['expiration'], "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                remaining_time = expiration - now
                if remaining_time.total_seconds() <= 0:
                    self.result_label.setText('Code has expired.')
                else:
                    hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    self.result_label.setText(f'Time left: {int(hours)}h {int(minutes)}m {int(seconds)}s')
            else:
                self.result_label.setText('Invalid code.')

    def input_style(self):
        return "background-color: #444; color: #ddd; border: 1px solid #666; border-radius: 5px; padding: 5px;"

    def button_style(self):
        return "background-color: #555; color: #ddd; border: 1px solid #666; border-radius: 5px; padding: 10px;"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiscountApp()
    window.show()
    sys.exit(app.exec_())
