from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QFont, QIcon

from .utils import *


class StepItem(QListWidgetItem):
    def __init__(self,  text="No text") -> None:
        super().__init__(text)
        self.setIcon(QIcon(get_data("../icons/right-arrow.png")))
        


class StepsWidget(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        
        step1 = StepItem("P0 at depth 6")
        self.addItem(step1)
        step2 = StepItem("Euler at depth 3")
        self.addItem(step2)
        step3 = StepItem("CZ at depth 6")
        self.addItem(step3)
        step4 = StepItem("HH at depth 1")
        
        self.addItem(step4)
        step4.setSelected(True)


