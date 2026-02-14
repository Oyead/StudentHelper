import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel,
    QApplication, QMenu, QFileDialog, QFrame, QScrollArea, QStackedWidget
)
from PyQt5.QtGui import QPixmap, QFont, QCursor
from PyQt5.QtCore import Qt
from utils import select_file, convert, merge_pdfs

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Helper Pro")
        self.setMinimumSize(1200, 800) 

        # Colors
        self.color_bg = "#000000"
        self.color_card_bg = "#A2D5C6"
        self.color_accent = "#CFFFE2"
        self.color_text_main = "#F6F6F6"

        self.setObjectName("MainWindow")
        self.setStyleSheet(f"""
            QWidget#MainWindow {{
                background-color: {self.color_bg};
            }}
            QWidget {{ color: {self.color_text_main}; }}
        """)

        self.selected_files = []
        self.init_ui()
        self.setAcceptDrops(True)

    def init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # --- Navigation Bar ---
        nav_container = QWidget()
        nav = QHBoxLayout(nav_container)
        nav.setContentsMargins(60, 40, 60, 20)

        self.nav_buttons = []
        for text in ["File Conversion", "Option B", "Option C"]:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setFixedHeight(55)
            btn.setFont(QFont("Inter", 12, QFont.Bold))
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet(self.nav_style())
            btn.clicked.connect(lambda _, t=text: self.switch_page(t))
            nav.addWidget(btn)
            self.nav_buttons.append(btn)

        # --- Stacked Content Area ---
        self.stack = QStackedWidget()
        
        # Create Pages
        self.conversion_page = self.create_conversion_page()
        self.placeholder_b = self.create_placeholder_page("Option B Content")
        self.placeholder_c = self.create_placeholder_page("Option C Content")

        self.stack.addWidget(self.conversion_page)
        self.stack.addWidget(self.placeholder_b)
        self.stack.addWidget(self.placeholder_c)

        root.addWidget(nav_container)
        root.addWidget(self.stack)

        # Set Initial State
        self.nav_buttons[0].setChecked(True)
        self.stack.setCurrentIndex(0)

    def create_conversion_page(self):
        page = QFrame()
        page_layout = QVBoxLayout(page)
        
        card = QFrame()
        card.setFixedWidth(1000)
        layout = QVBoxLayout(card)
        layout.setSpacing(30)

        title = QLabel("File Conversion")
        title.setFont(QFont("Josefin Sans", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color:{self.color_accent}")
        layout.addWidget(title)

        # Buttons Row
        row = QHBoxLayout()
        self.select_btn = QPushButton("Select Files")
        self.select_btn.setFixedSize(260, 65)
        self.select_btn.setStyleSheet(self.btn_style(self.color_card_bg))
        self.select_btn.clicked.connect(self.handle_file_selection)

        self.convert_btn = QPushButton("CONVERT ALL TO")
        self.convert_btn.setFixedSize(260, 65)
        self.convert_btn.setVisible(False)
        self.convert_btn.setStyleSheet(self.btn_style(self.color_accent))

        self.menu = QMenu(self)
        self.menu.setStyleSheet(self.menu_style())
        self.convert_btn.setMenu(self.menu)

        row.addStretch()
        row.addWidget(self.select_btn)
        row.addSpacing(30)
        row.addWidget(self.convert_btn)
        row.addStretch()
        layout.addLayout(row)

        # Scroll Area for Files
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)
        self.scroll.setStyleSheet("border:none; background:transparent;")

        self.scroll_widget = QWidget()
        self.files_layout = QVBoxLayout(self.scroll_widget)
        self.files_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.scroll_widget)

        layout.addWidget(self.scroll)

        # --- Clear All Button ---
        self.clear_all_btn = QPushButton("CLEAR ALL")
        self.clear_all_btn.setFixedWidth(200)
        self.clear_all_btn.setFixedHeight(40)
        self.clear_all_btn.setFont(QFont("Inter", 10, QFont.Bold))
        self.clear_all_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.clear_all_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: #E63946;
                border: 2px solid #E63946;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background: #E63946;
                color: white;
            }}
        """)
        self.clear_all_btn.setVisible(False)
        self.clear_all_btn.clicked.connect(self.clear_all_files)
        
        # Center the Clear All button below the scroll area
        clear_row = QHBoxLayout()
        clear_row.addStretch()
        clear_row.addWidget(self.clear_all_btn)
        clear_row.addStretch()
        layout.addLayout(clear_row)

        # Center the card in the page
        center_h = QHBoxLayout()
        center_h.addStretch()
        center_h.addWidget(card)
        center_h.addStretch()
        page_layout.addLayout(center_h)
        
        return page

    def create_placeholder_page(self, text):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFont(QFont("Inter", 20))
        return lbl

    def switch_page(self, option):
        # Update button highlighting
        for b in self.nav_buttons:
            b.setChecked(b.text() == option)
        
        # Switch stack index
        mapping = {"File Conversion": 0, "Option B": 1, "Option C": 2}
        self.stack.setCurrentIndex(mapping.get(option, 0))

    def handle_file_selection(self):
        paths = select_file()
        if not paths:
            return

        for path in paths:
            if path not in self.selected_files:
                self.selected_files.append(path)
                row_widget = self.create_file_row(path)
                self.files_layout.addWidget(row_widget)

        if self.selected_files:
            self.convert_btn.setVisible(True)
            self.clear_all_btn.setVisible(True)
            # Update menu options based on the first file's type
            ext = os.path.splitext(self.selected_files[0])[1].lower()
            self.update_menu(ext)
    def dragEnterEvent(self, event):
     if event.mimeData().hasUrls():
        event.acceptProposedAction()

    def dropEvent(self, event):
     for url in event.mimeData().urls():
        path = url.toLocalFile()
        if os.path.isfile(path) and path not in self.selected_files:
            self.selected_files.append(path)
            row = self.create_file_row(path)
            self.files_layout.addWidget(row)

     if self.selected_files:
        self.convert_btn.setVisible(True)
        self.clear_all_btn.setVisible(True)
        ext = os.path.splitext(self.selected_files[0])[1].lower()
        self.update_menu(ext)

    def create_file_row(self, path):
        frame = QFrame()
        frame.setFixedHeight(80)
        frame.setStyleSheet(f"background:{self.color_card_bg}; border-radius:15px;")

        h = QHBoxLayout(frame)
        h.setContentsMargins(20, 0, 20, 0)

        icon = QLabel()
        icon.setPixmap(QPixmap(self.icon_path(path)).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        name = QLabel(os.path.basename(path).upper())
        name.setFont(QFont("Inter", 11, QFont.Bold))
        name.setStyleSheet("color:black;")

        size = QLabel(self.format_size(os.path.getsize(path)))
        size.setStyleSheet("color:black;")

        remove = QPushButton("✕")
        remove.setFixedSize(35, 35)
        remove.setCursor(QCursor(Qt.PointingHandCursor))
        remove.setStyleSheet("background:#E63946; color:white; border-radius:17px; font-weight:bold;")
        remove.clicked.connect(lambda: self.remove_file(path, frame))

        h.addWidget(icon)
        h.addSpacing(15)
        h.addWidget(name)
        h.addStretch()
        h.addWidget(size)
        h.addSpacing(20)
        h.addWidget(remove)

        return frame

    def remove_file(self, path, widget):
        if path in self.selected_files:
            self.selected_files.remove(path)
        widget.deleteLater()
        if not self.selected_files:
            self.convert_btn.setVisible(False)
            self.clear_all_btn.setVisible(False)

    def clear_all_files(self):
        # Remove all widgets from the layout
        while self.files_layout.count():
            item = self.files_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.selected_files.clear()
        self.convert_btn.setVisible(False)
        self.clear_all_btn.setVisible(False)

    def update_menu(self, ext):
     self.menu.clear()

     if ext == ".pdf":
        for label, key in [
            ("DOCX", "docx"),
            ("TXT", "txt"),
            ("HTML", "html"),
            ("MERGE PDFs", "merge")
        ]:
            act = self.menu.addAction(label)
            act.triggered.connect(lambda _, k=key: self.convert_files(k))
        return

     mapping = {
        ".docx": ["pdf", "txt", "html"],
        ".txt": ["pdf", "docx", "html"],
        ".html": ["pdf", "docx", "txt"]
    }

     for fmt in mapping.get(ext, []):
        act = self.menu.addAction(fmt.upper())
        act.triggered.connect(lambda _, f=fmt: self.convert_files(f))


    def convert_files(self, fmt):
     out = QFileDialog.getExistingDirectory(self, "Select Output Folder")
     if not out:
        return

     try:
        if fmt == "merge":
             from utils import merge_pdfs
             pdfs = [p for p in self.selected_files if p.lower().endswith(".pdf")]
             merge_pdfs(pdfs, out)
             return

        for p in self.selected_files:
            convert(p, out, fmt)

     except Exception as e:
        print(e)


    def icon_path(self, path):
        ext = os.path.splitext(path)[1].lower()
        return {
            ".pdf": "assets/pdf-icon.png",
            ".docx": "assets/word-icon.png",
            ".txt": "assets/txt-icon.png",
            ".html": "assets/html-icon.png"
        }.get(ext, "assets/generic-icon.png")

    def format_size(self, b):
        if b < 1024: return f"{b} B"
        if b < 1024**2: return f"{b/1024:.2f} KB"
        return f"{b/1024**2:.2f} MB"

    def nav_style(self):
        return f"""
            QPushButton {{
                border: 2px solid {self.color_card_bg};
                border-radius: 12px;
                padding: 0 40px;
                color: {self.color_card_bg};
                background: transparent;
            }}
            QPushButton:checked {{
                background: {self.color_accent};
                color: black;
            }}
        """

    def btn_style(self, bg):
        return f"""
            QPushButton {{
                background: {bg};
                color: black;
                border-radius: 15px;
                font-weight: bold;
            }}
            QPushButton::menu-indicator {{ image: none; }}
        """

    def menu_style(self):
        return f"""
            QMenu {{
                background: black;
                color: white;
                border: 2px solid {self.color_accent};
            }}
            QMenu::item:selected {{
                background: {self.color_accent};
                color: black;
            }}
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())