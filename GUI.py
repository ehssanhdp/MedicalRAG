from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from main import process_question  # Adjust import based on your main processing script


class ClinicalAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("دستیار سوالات بالینی")
        self.resize(600, 700)

        # Persian font
        persian_font = QFont("B Nazanin", 30, QFont.Bold)  # Replace with a Persian-compatible font

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: #f7f7f7;
                font-size: 14px;
            }
            QLabel {
                color: #2c3e50;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)

        # Set layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header label
        header_label = QLabel("به دستیار سوالات بالینی خوش آمدید")
        header_label.setFont(QFont("B Nazanin", 25, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Input label
        self.question_label = QLabel("سوال بالینی خود را وارد کنید:")
        self.question_label.setFont(persian_font)
        self.question_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.question_label)

        # Text input for the question
        self.question_input = QTextEdit()
        self.question_input.setFont(persian_font)
        self.question_input.setAlignment(Qt.AlignLeft)
        self.question_input.setLayoutDirection(Qt.RightToLeft)
        layout.addWidget(self.question_input)

        # Submit button
        self.submit_button = QPushButton("ارسال")
        self.submit_button.setFont(persian_font)
        self.submit_button.clicked.connect(self.handle_submit)
        layout.addWidget(self.submit_button)

        # Context label and output
        self.context_label = QLabel("متن مرتبط:")
        self.context_label.setFont(persian_font)
        self.context_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.context_label)

        self.context_output = QTextEdit()
        self.context_output.setFont(persian_font)
        self.context_output.setAlignment(Qt.AlignRight)
        self.context_output.setLayoutDirection(Qt.RightToLeft)
        self.context_output.setReadOnly(True)
        layout.addWidget(self.context_output)

        # Response label and output
        self.response_label = QLabel("پاسخ تولید شده:")
        self.response_label.setFont(persian_font)
        self.response_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.response_label)

        self.response_output = QTextEdit()
        self.response_output.setFont(persian_font)
        self.response_output.setAlignment(Qt.AlignRight)
        self.response_output.setLayoutDirection(Qt.RightToLeft)
        self.response_output.setReadOnly(True)
        layout.addWidget(self.response_output)

        # Set main layout
        self.setLayout(layout)

    def handle_submit(self):
        # Get the user question
        question = self.question_input.toPlainText().strip()

        if not question:
            QMessageBox.warning(self, "خطا در ورودی", "لطفاً یک سوال بالینی وارد کنید.")
            return

        try:
            # Process the input and get results
            context, response = process_question(question)

            # Display the results
            self.context_output.setPlainText(context)
            self.response_output.setPlainText(response)
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"یک خطا رخ داده است: {e}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    assistant = ClinicalAssistant()
    assistant.show()
    sys.exit(app.exec_())