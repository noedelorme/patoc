from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QRect
from .main_window import MainWindow

class Patoc(QApplication):
    """The Patoc application"""

    def __init__(self) -> None:
        super().__init__()

        self.setApplicationName("Patoc")

        self.main_window = MainWindow()
        self.main_window.setWindowTitle("Patoc")
        screenrect = self.primaryScreen().geometry()
        self.main_window.move(screenrect.right(), screenrect.top())
        self.main_window.show()
        