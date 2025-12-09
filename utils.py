import os
from PyQt5.QtWidgets import QFileDialog

def select_file():
    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select a file",
        "",
        "All files (*.*)"
    )
    if file_path:
        print("Selected file:", file_path)
        fileType = os.path.splitext(file_path)[1][1:]
        fileName = os.path.basename(file_path)
        print("File Type:", fileType)
        print("File Name:", fileName)
        return file_path
    return None