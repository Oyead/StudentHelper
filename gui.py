from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QTextEdit, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from utils import select_file, convert
import sys
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Helper")
        self.setWindowIcon(QIcon("assets/book.png"))
        self.showMaximized()

        # Option Buttons
        self.button1 = QPushButton("File type conversion")
        self.button2 = QPushButton("Option B")
        self.button3 = QPushButton("Option C")

        for button in (self.button1, self.button2, self.button3):
            button.setFixedHeight(50)
            button.setStyleSheet("font-size: 24px;")

        self.button1.clicked.connect(lambda: self.show_content("File type conversion"))
        self.button2.clicked.connect(lambda: self.show_content("Option B"))
        self.button3.clicked.connect(lambda: self.show_content("Option C"))

        # Layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.button1)
        top_layout.addWidget(self.button2)
        top_layout.addWidget(self.button3)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)

        self.selected_file_path = None

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.content_area)
        self.setLayout(main_layout)

    # Utility Methods
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
            elif item.layout():
                self.clear_layout(item.layout())

    # Content Display
    def show_content(self, option):
        self.clear_layout(self.content_layout)

        if option == "File type conversion":
            content_row = QHBoxLayout()

            # Add file button
            add_file_btn = QPushButton("Add a file")
            add_file_btn.setFixedSize(150, 50)
            add_file_btn.setStyleSheet("font-size: 18px;")
            add_file_btn.clicked.connect(self.handle_file_selection)
            content_row.addWidget(add_file_btn, alignment=Qt.AlignLeft)

            # File info
            self.file_info_label = QLabel("No file selected")
            self.file_info_label.setStyleSheet("font-size: 18px; padding: 10px;")
            content_row.addWidget(self.file_info_label, alignment=Qt.AlignLeft)

            # Convert button
            self.convert_button = QPushButton("Convert to ▼")
            self.convert_button.setFixedSize(150, 50)
            self.convert_button.setStyleSheet("font-size: 18px;")
            self.convert_button.setVisible(False)

            # Dropdown menu
            self.convert_menu = QMenu(self)
            html_action = self.convert_menu.addAction("HTML")
            txt_action = self.convert_menu.addAction("TXT")
            pdf_action = self.convert_menu.addAction("PDF")

            html_action.triggered.connect(lambda: self.handle_conversion("html"))
            txt_action.triggered.connect(lambda: self.handle_conversion("txt"))
            pdf_action.triggered.connect(lambda: self.handle_conversion("pdf"))

            self.convert_button.setMenu(self.convert_menu)
            content_row.addWidget(self.convert_button, alignment=Qt.AlignLeft)

            self.content_layout.addLayout(content_row)

            # Preview section
            preview_label = QLabel("File Preview:")
            preview_label.setStyleSheet("font-size: 20px; font-weight: bold; padding-top: 20px;")
            self.content_layout.addWidget(preview_label)

            self.preview_area = QTextEdit()
            self.preview_area.setReadOnly(True)
            self.preview_area.setStyleSheet("font-size: 14px; border: 1px solid #ccc; padding: 10px;")
            self.preview_area.setPlaceholderText("Select a file to preview its contents...")
            self.content_layout.addWidget(self.preview_area, stretch=1)

            # Restore previous file if any
            if self.selected_file_path:
                self.update_file_info(self.selected_file_path)
                self.update_preview(self.selected_file_path)
                self.update_conversion_button(self.selected_file_path)

        elif option == "Option B":
            label = QLabel("Option B Interface")
            label.setStyleSheet("font-size: 18px;")
            self.content_layout.addWidget(label)
        elif option == "Option C":
            label = QLabel("Option C Interface")
            label.setStyleSheet("font-size: 18px;")
            self.content_layout.addWidget(label)

    # File Handling
    def handle_file_selection(self):
        file_path = select_file()
        if file_path:
            self.selected_file_path = file_path
            self.update_file_info(file_path)
            self.update_preview(file_path)
            self.update_conversion_button(file_path)

    def update_file_info(self, file_path):
        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_path)[1][1:] or "No extension"
        file_size = os.path.getsize(file_path)

        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"

        self.file_info_label.setText(f"Selected: {file_name} | Type: {file_type} | Size: {size_str}")

    def update_preview(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        text_exts = ['.txt', '.py', '.js', '.html', '.css', '.json', '.xml', 
                     '.csv', '.md', '.log', '.ini', '.cfg', '.conf', '.yml', '.yaml']

        if file_ext in text_exts:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()

            if len(content) > 10000:
                content = content[:10000] + "\n\n... (Preview truncated, file is too large)"
            self.preview_area.setPlainText(content)
        else:
            self.preview_area.setPlainText(
                f"File type '{file_ext}' is not previewable as text.\n\n"
                f"File: {os.path.basename(file_path)}\n"
                f"Path: {file_path}\n"
                f"Size: {os.path.getsize(file_path)} bytes"
            )

    def update_conversion_button(self, file_path):
    # Supported conversions depending on input type
       SUPPORTED_CONVERSIONS = {
        ".docx": ["pdf", "txt", "html"],
        ".doc": ["pdf", "txt", "html"],
        ".pdf": ["txt", "html", "docx"],
        ".txt":["pdf","docx","html"],
        ".html":["pdf","docx","txt"]
        }

       file_ext = os.path.splitext(file_path)[1].lower()

       if file_ext not in SUPPORTED_CONVERSIONS:
         self.convert_button.setVisible(False)
         return

       self.convert_button.setVisible(True)

        # Clear existing menu
       self.convert_menu.clear()

       for fmt in SUPPORTED_CONVERSIONS[file_ext]:
         action = self.convert_menu.addAction(fmt.upper())
         action.triggered.connect(lambda checked, f=fmt: self.handle_conversion(f))

    def select_output_file(self, target_format):
     from PyQt5.QtWidgets import QFileDialog
     app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

     base_name = os.path.splitext(
        os.path.basename(self.selected_file_path)
     )[0]

     default_path = os.path.join(app_dir, f"{base_name}.{target_format}")

     file_path, _ = QFileDialog.getSaveFileName(
         self,
         "Save converted file",
         default_path,
         f"{target_format.upper()} Files (*.{target_format});;All Files (*)"
     )

     return file_path

    # Conversion
    def handle_conversion(self, target_format):
        
        if not self.selected_file_path:
            return
        out_path = self.select_output_file(target_format)
        if not out_path:
            return
        output_dir = os.path.dirname(out_path)
        try:
            convert(self.selected_file_path, output_dir, target_format)
        except Exception as e:
            print(f"Conversion failed: {e}")

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
