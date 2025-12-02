from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from utils import select_file
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Helper")
        self.setWindowIcon(QIcon("assets/book.png"))
        self.showMaximized()

        # --- Option Buttons ---
        self.button1 = QPushButton("File type conversion")
        self.button2 = QPushButton("Option B")
        self.button3 = QPushButton("Option C")

        for button in (self.button1, self.button2, self.button3):
            button.setFixedHeight(50)
            button.setStyleSheet("font-size: 24px;")

        # Connect buttons
        self.button1.clicked.connect(lambda: self.show_content("File type conversion"))
        self.button2.clicked.connect(lambda: self.show_content("Option B"))
        self.button3.clicked.connect(lambda: self.show_content("Option C"))

        # --- Layout ---
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.button1)
        top_layout.addWidget(self.button2)
        top_layout.addWidget(self.button3)

        # Content area (dynamic)
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.content_area)
        self.setLayout(main_layout)

    def clear_layout(self, layout):
        """Recursively clear all widgets and nested layouts."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                self.clear_layout(item.layout())

    def show_content(self, option):
        # Clear previous content
        self.clear_layout(self.content_layout)

        if option == "File type conversion":
            # Horizontal row for file conversion
            content_row = QHBoxLayout()

            # "Add a file" button
            add_file_button = QPushButton("Add a file")
            add_file_button.setFixedSize(150, 50)
            add_file_button.setStyleSheet("font-size: 18px;")
            add_file_button.clicked.connect(select_file)
            content_row.addWidget(add_file_button, alignment=Qt.AlignLeft)

            # Placeholder label
            info_label = QLabel("")
            info_label.setStyleSheet("font-size: 18px;")
            content_row.addWidget(info_label, alignment=Qt.AlignLeft)

            # Add horizontal row to main content
            self.content_layout.addLayout(content_row)

        elif option == "Option B":
            label = QLabel("Option B Interface")
            label.setStyleSheet("font-size: 18px;")
            self.content_layout.addWidget(label)

        elif option == "Option C":
            label = QLabel("Option C Interface")
            label.setStyleSheet("font-size: 18px;")
            self.content_layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
