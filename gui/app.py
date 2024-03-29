from PySide6.QtWidgets import QApplication
from .mainwindow import MainWindow

class Patoc(QApplication):
    """The Patoc application"""

    def __init__(self) -> None:
        super().__init__()

        self.main_window = MainWindow()
        self.main_window.show()