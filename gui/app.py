from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QRect

from .main_window import MainWindow
from .utils import *


class Patoc(QApplication):
    """The Patoc application"""

    def __init__(self) -> None:
        super().__init__()

        self.setApplicationName("Patoc")
        self.setDesktopFileName('Patoc')
        self.setApplicationVersion('0.1')
        self.main_window = MainWindow(self)
        self.main_window.setWindowTitle("Patoc")
        self.main_window.setWindowIcon(QIcon(get_data('../icons/logo.png')))
        self.setWindowIcon(self.main_window.windowIcon())
        # screenrect = self.primaryScreen().geometry()
        # self.main_window.move(screenrect.right(), screenrect.top())
        self.main_window.show()
        