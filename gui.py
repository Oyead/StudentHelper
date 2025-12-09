from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QTextEdit, QScrollArea, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from utils import select_file
import sys
import os

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
        
        # Store selected file path
        self.selected_file_path = None

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
            add_file_button.clicked.connect(self.handle_file_selection)
            content_row.addWidget(add_file_button, alignment=Qt.AlignLeft)

            # File info label
            self.file_info_label = QLabel("No file selected")
            self.file_info_label.setStyleSheet("font-size: 18px; padding: 10px;")
            content_row.addWidget(self.file_info_label, alignment=Qt.AlignLeft)

            # Conversion button with dropdown (initially hidden)
            self.convert_button = QPushButton("Convert to ▼")
            self.convert_button.setFixedSize(150, 50)
            self.convert_button.setStyleSheet("font-size: 18px;")
            self.convert_button.setVisible(False)
            
            # Create dropdown menu
            self.convert_menu = QMenu(self)
            html_action = self.convert_menu.addAction("HTML")
            txt_action = self.convert_menu.addAction("TXT")
            pdf_action = self.convert_menu.addAction("PDF")
            
            # Connect menu actions
            html_action.triggered.connect(lambda: self.handle_conversion("html"))
            txt_action.triggered.connect(lambda: self.handle_conversion("txt"))
            pdf_action.triggered.connect(lambda: self.handle_conversion("pdf"))
            
            self.convert_button.setMenu(self.convert_menu)
            content_row.addWidget(self.convert_button, alignment=Qt.AlignLeft)

            # Add horizontal row to main content
            self.content_layout.addLayout(content_row)
            
            # Preview section
            preview_label = QLabel("File Preview:")
            preview_label.setStyleSheet("font-size: 20px; font-weight: bold; padding-top: 20px;")
            self.content_layout.addWidget(preview_label)
            
            # Preview area
            self.preview_area = QTextEdit()
            self.preview_area.setReadOnly(True)
            self.preview_area.setStyleSheet("font-size: 14px; border: 1px solid #ccc; padding: 10px;")
            self.preview_area.setPlaceholderText("Select a file to preview its contents...")
            self.content_layout.addWidget(self.preview_area, stretch=1)
            
            # If a file was previously selected, restore its state
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
    
    def handle_file_selection(self):
        """Handle file selection and update preview."""
        file_path = select_file()
        if file_path:
            self.selected_file_path = file_path
            self.update_file_info(file_path)
            self.update_preview(file_path)
            self.update_conversion_button(file_path)
    
    def update_file_info(self, file_path):
        """Update the file information label."""
        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_path)[1][1:] or "No extension"
        file_size = os.path.getsize(file_path)
        
        # Format file size
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        
        info_text = f"Selected: {file_name} | Type: {file_type} | Size: {size_str}"
        self.file_info_label.setText(info_text)
    
    def update_preview(self, file_path):
        """Update the preview area with file contents."""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Text-based file extensions
            text_extensions = ['.txt', '.py', '.js', '.html', '.css', '.json', '.xml', 
                             '.csv', '.md', '.log', '.ini', '.cfg', '.conf', '.yml', '.yaml']
            
            if file_ext in text_extensions:
                # Try to read as text
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Limit preview to first 10000 characters
                    if len(content) > 10000:
                        content = content[:10000] + "\n\n... (Preview truncated, file is too large)"
                    self.preview_area.setPlainText(content)
                except UnicodeDecodeError:
                    # Try with different encoding
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            content = f.read()
                        if len(content) > 10000:
                            content = content[:10000] + "\n\n... (Preview truncated, file is too large)"
                        self.preview_area.setPlainText(content)
                    except Exception as e:
                        self.preview_area.setPlainText(f"Error reading file: {str(e)}")
            else:
                # Binary or unsupported file type
                self.preview_area.setPlainText(
                    f"File type '{file_ext}' is not previewable as text.\n\n"
                    f"File: {os.path.basename(file_path)}\n"
                    f"Path: {file_path}\n"
                    f"Size: {os.path.getsize(file_path)} bytes"
                )
        except Exception as e:
            self.preview_area.setPlainText(f"Error loading preview: {str(e)}")
    
    def update_conversion_button(self, file_path):
        """Show/hide conversion button based on file type."""
        file_ext = os.path.splitext(file_path)[1].lower()
        word_extensions = ['.doc', '.docx']
        
        if file_ext in word_extensions:
            self.convert_button.setVisible(True)
        else:
            self.convert_button.setVisible(False)
    
    def handle_conversion(self, target_format):
        """Handle file conversion to the specified format."""
        if not self.selected_file_path:
            return
        
        file_name = os.path.basename(self.selected_file_path)
        file_base = os.path.splitext(file_name)[0]
        file_dir = os.path.dirname(self.selected_file_path)
        
        # Determine output file extension
        ext_map = {
            "html": ".html",
            "txt": ".txt",
            "pdf": ".pdf"
        }
        
        output_ext = ext_map.get(target_format.lower(), ".txt")
        output_path = os.path.join(file_dir, f"{file_base}{output_ext}")
        
        # TODO: Implement actual conversion logic
        # For now, just show a message
        print(f"Converting {self.selected_file_path} to {target_format.upper()}")
        print(f"Output path: {output_path}")
        
        # You can add actual conversion logic here using libraries like:
        # - python-docx for Word files
        # - pdfkit or reportlab for PDF conversion
        # - html2text or similar for HTML conversion


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
