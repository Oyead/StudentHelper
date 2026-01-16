from PyQt5.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QMenu, QFileDialog
)
from PyQt5.QtGui import QIcon, QPixmap, QCursor
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
        self.setStyleSheet("background-color: #1e1e2f; color: #ffffff;")

        # Option Buttons
        self.button1 = QPushButton("File Conversion")
        self.button2 = QPushButton("Option B")
        self.button3 = QPushButton("Option C")
        for btn in (self.button1, self.button2, self.button3):
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    border-radius: 15px;
                    background-color: #2e3b55;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #ffffff;
                    color: #2e3b55;
                }
            """)
        self.button1.clicked.connect(lambda: self.show_content("File Conversion"))
        self.button2.clicked.connect(lambda: self.show_content("Option B"))
        self.button3.clicked.connect(lambda: self.show_content("Option C"))

        # Layout
        top_layout = QHBoxLayout()
        top_layout.addSpacing(20)
        top_layout.addWidget(self.button1)
        top_layout.addWidget(self.button2)
        top_layout.addWidget(self.button3)
        top_layout.addSpacing(20)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)

        self.selected_file_path = None

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.content_area)
        self.setLayout(main_layout)

    # --- Utility ---
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    # --- Content Display ---
    def show_content(self, option):
        self.clear_layout(self.content_layout)

        if option == "File Conversion":
            content_row = QHBoxLayout()

            # Add file button
            add_file_btn = QPushButton("Add File")
            add_file_btn.setFixedSize(150, 50)
            add_file_btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    border-radius: 12px;
                    background-color: #3f51b5;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #ffffff;
                    color: #3f51b5;
                }
            """)
            add_file_btn.clicked.connect(self.handle_file_selection)
            content_row.addWidget(add_file_btn, alignment=Qt.AlignLeft)

            # Convert Button
            self.convert_button = QPushButton("Convert")
            self.convert_button.setFixedSize(150, 50)
            self.convert_button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    border-radius: 12px;
                    background-color: #3f51b5;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background-color: #ffffff;
                    color: #3f51b5;
                }
            """)
            self.convert_button.setVisible(False)

            # Convert Menu
            self.convert_menu = QMenu(self)
            self.convert_menu.setStyleSheet("""
                QMenu {
                    background-color: #2e3b55;
                    color: #ffffff;
                    border-radius: 10px;
                    padding: 5px;
                }
                QMenu::item {
                    padding: 5px 20px;
                    border-radius: 8px;
                }
                QMenu::item:selected {
                    background-color: #ffffff;
                    color: #2e3b55;
                }
            """)
            self.convert_button.setMenu(self.convert_menu)

            content_row.addWidget(self.convert_button, alignment=Qt.AlignLeft)

            self.content_layout.addLayout(content_row)
            self.content_layout.addSpacing(20)

            # File Preview
            preview_label = QLabel("File Preview")
            preview_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
            self.content_layout.addWidget(preview_label)

            self.preview_layout = QVBoxLayout()
            self.preview_layout.setAlignment(Qt.AlignHCenter)

            # File Icon
            self.file_icon_label = QLabel()
            self.file_icon_label.setFixedSize(100, 100)
            self.file_icon_label.setScaledContents(True)
            self.preview_layout.addWidget(self.file_icon_label, alignment=Qt.AlignHCenter)

            # Filename
            self.file_name_label = QLabel("No file selected")
            self.file_name_label.setStyleSheet("font-size: 16px; color: #ffffff; padding-top: 5px;")
            self.file_name_label.setCursor(QCursor(Qt.PointingHandCursor))
            self.file_name_label.installEventFilter(self)
            self.preview_layout.addWidget(self.file_name_label, alignment=Qt.AlignHCenter)

            # File Info
            self.file_info_preview_label = QLabel("")
            self.file_info_preview_label.setStyleSheet("font-size: 14px; color: #a0a0a0; padding-top: 5px;")
            self.file_info_preview_label.setCursor(QCursor(Qt.PointingHandCursor))
            self.file_info_preview_label.installEventFilter(self)
            self.preview_layout.addWidget(self.file_info_preview_label, alignment=Qt.AlignHCenter)

            self.content_layout.addLayout(self.preview_layout)
        else:
            label = QLabel(f"{option} Interface")
            label.setStyleSheet("font-size: 18px; color: #ffffff;")
            self.content_layout.addWidget(label)

    # --- File Handling ---
    def handle_file_selection(self):
        file_path = select_file()
        if file_path:
            self.selected_file_path = file_path
            self.update_file_info(file_path)
            self.update_preview_icon(file_path)
            self.update_conversion_button(file_path)

    def update_file_info(self, file_path):
        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_path)[1][1:] or "No extension"
        file_size = os.path.getsize(file_path)
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024*1024:
            size_str = f"{file_size/1024:.2f} KB"
        else:
            size_str = f"{file_size/(1024*1024):.2f} MB"

        info_text = f"Type: {file_type} | Size: {size_str}"
        self.file_name_label.setText(file_name)
        self.file_info_preview_label.setText(info_text)

    def update_preview_icon(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        icon_map = {
            ".pdf": "assets/pdf_icon.png",
            ".docx": "assets/word_icon.png",
            ".txt": "assets/txt_icon.png",
            ".html": "assets/html_icon.png",
        }
        icon_path = icon_map.get(ext, "assets/file_icon.png")
        self.file_icon_label.setPixmap(QPixmap(icon_path))

    # --- Conversion ---
    def update_conversion_button(self, file_path):
        SUPPORTED_CONVERSIONS = {
            ".docx": ["pdf", "txt", "html"],
            ".doc": ["pdf", "txt", "html"],
            ".pdf": ["txt", "html", "docx"],
            ".txt": ["pdf", "docx", "html"],
            ".html": ["pdf", "docx", "txt"]
        }

        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in SUPPORTED_CONVERSIONS:
            self.convert_button.setVisible(False)
            return

        self.convert_button.setVisible(True)
        self.convert_menu.clear()
        for fmt in SUPPORTED_CONVERSIONS[file_ext]:
            action = self.convert_menu.addAction(fmt.upper())
            action.triggered.connect(lambda checked, f=fmt: self.handle_conversion(f))

    def select_output_file(self, target_format):
        app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        base_name = os.path.splitext(os.path.basename(self.selected_file_path))[0]
        default_path = os.path.join(app_dir, f"{base_name}.{target_format}")

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save converted file",
            default_path,
            f"{target_format.upper()} Files (*.{target_format});;All Files (*)"
        )
        return file_path

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

    # --- Event Filter for Hover Highlight ---
    def eventFilter(self, source, event):
        if event.type() == event.Enter:
            source.setStyleSheet("color: #3f51b5;")
        elif event.type() == event.Leave:
            if source == self.file_name_label:
                source.setStyleSheet("font-size: 16px; color: #ffffff; padding-top: 5px;")
            elif source == self.file_info_preview_label:
                source.setStyleSheet("font-size: 14px; color: #a0a0a0; padding-top: 5px;")
        return super().eventFilter(source, event)

# --- Main ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
