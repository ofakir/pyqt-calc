import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Calculator")
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLineEdit {
                background-color: #3c3c3c;
                color: white;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 10px;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: 2px solid #555;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
            QPushButton#operator {
                background-color: #ff9500;
                color: white;
            }
            QPushButton#operator:hover {
                background-color: #ffaa33;
            }
            QPushButton#equals {
                background-color: #007aff;
                color: white;
            }
            QPushButton#equals:hover {
                background-color: #0056cc;
            }
            QPushButton#clear {
                background-color: #ff3b30;
                color: white;
            }
            QPushButton#clear:hover {
                background-color: #ff5a4f;
            }
        """)
        
        self.current_number = ""
        self.first_number = None
        self.operation = None
        self.new_number = True
        self.expression = ""  # Store the full expression
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Display
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setText("0")
        layout.addWidget(self.display)
        
        # Buttons grid
        buttons_layout = QGridLayout()
        
        # Create buttons manually for better control
        # Row 1: C, ±, %, ÷
        buttons_layout.addWidget(self.create_button('C'), 0, 0)
        buttons_layout.addWidget(self.create_button('±'), 0, 1)
        buttons_layout.addWidget(self.create_button('%'), 0, 2)
        buttons_layout.addWidget(self.create_button('÷'), 0, 3)
        
        # Row 2: 7, 8, 9, ×
        buttons_layout.addWidget(self.create_button('7'), 1, 0)
        buttons_layout.addWidget(self.create_button('8'), 1, 1)
        buttons_layout.addWidget(self.create_button('9'), 1, 2)
        buttons_layout.addWidget(self.create_button('×'), 1, 3)
        
        # Row 3: 4, 5, 6, -
        buttons_layout.addWidget(self.create_button('4'), 2, 0)
        buttons_layout.addWidget(self.create_button('5'), 2, 1)
        buttons_layout.addWidget(self.create_button('6'), 2, 2)
        buttons_layout.addWidget(self.create_button('-'), 2, 3)
        
        # Row 4: 1, 2, 3, +
        buttons_layout.addWidget(self.create_button('1'), 3, 0)
        buttons_layout.addWidget(self.create_button('2'), 3, 1)
        buttons_layout.addWidget(self.create_button('3'), 3, 2)
        buttons_layout.addWidget(self.create_button('+'), 3, 3)
        
        # Row 5: 0 (spans 2 columns), ., =
        buttons_layout.addWidget(self.create_button('0'), 4, 0, 1, 2)
        buttons_layout.addWidget(self.create_button('.'), 4, 2)
        buttons_layout.addWidget(self.create_button('='), 4, 3)
        
        layout.addLayout(buttons_layout)
    
    def create_button(self, text):
        """Create a button with proper styling"""
        button = QPushButton(text)
        button.clicked.connect(self.button_clicked)
        
        # Set button styles
        if text in ['÷', '×', '-', '+']:
            button.setObjectName("operator")
        elif text == '=':
            button.setObjectName("equals")
        elif text == 'C':
            button.setObjectName("clear")
        
        return button
    
    def button_clicked(self):
        button = self.sender()
        text = button.text()
        
        if text.isdigit() or text == '.':
            self.handle_number(text)
        elif text in ['÷', '×', '-', '+']:
            self.handle_operator(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '±':
            self.negate()
        elif text == '%':
            self.percentage()
    
    def handle_number(self, number):
        if self.new_number:
            if number == '.':
                self.current_number = "0."
                self.expression += "0."
            else:
                self.current_number = number
                self.expression += number
            self.new_number = False
        else:
            if number == '.' and '.' in self.current_number:
                return
            self.current_number += number
            self.expression += number
        self.display.setText(self.expression)

    def handle_operator(self, operator):
        if self.current_number:
            # Only add operator if last character is not already an operator
            if self.expression and self.expression[-1] in '+-×÷':
                self.expression = self.expression[:-1] + operator
            else:
                self.expression += operator
            self.current_number = ""
            self.display.setText(self.expression)
            self.new_number = False

    def calculate(self):
        # Replace unicode operators with python equivalents
        expr = self.expression.replace('×', '*').replace('÷', '/')
        try:
            result = eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)
            self.display.setText(str(result))
            self.expression = str(result)
            self.current_number = str(result)
        except Exception:
            self.display.setText("Error")
            self.expression = ""
            self.current_number = ""
        self.new_number = True

    def clear(self):
        self.current_number = ""
        self.expression = ""
        self.new_number = True
        self.display.setText("0")
    
    def negate(self):
        if self.current_number and self.current_number != "0":
            if self.current_number.startswith('-'):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
            self.display.setText(self.current_number)
    
    def percentage(self):
        if self.current_number:
            value = float(self.current_number) / 100
            if value.is_integer():
                value = int(value)
            else:
                value = round(value, 8)
            self.current_number = str(value)
            self.display.setText(self.current_number)


def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 