from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .mainwindow import MainWindow

class Patoc(QApplication):
    """The Patoc application"""

    def __init__(self) -> None:
        super().__init__()

        self.setApplicationName("Patoc")
        self.setStyle("Universal")

        self.main_window = MainWindow()
        self.main_window.setWindowTitle("Patoc")
        self.main_window.show()