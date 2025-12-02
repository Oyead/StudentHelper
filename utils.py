import os
import tkinter as tk
from tkinter import filedialog
def select_file():
    file_path = filedialog.askopenfilename(title="Select a file",
    filetypes=(
        ("All files", "*.*"),
    ))
    print("Selected file:", file_path)
    fileType=os.path.splitext(file_path)[1][1:]
    fileName=os.path.basename(file_path)
    print("File Type:" ,fileType , "file")
    print("File Name:",fileName)