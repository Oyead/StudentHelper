from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Helper")
        self.setWindowIcon(QIcon("assets/book.png"))
        self.showMaximized()
