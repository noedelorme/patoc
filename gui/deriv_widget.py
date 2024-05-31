from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QFont, QIcon, QPainter, QPen, QPixmap

from .utils import *


class MatchItem(QListWidgetItem):
    def __init__(self,  text="No text", color="green") -> None:
        super().__init__(text)
        self.setIcon(QIcon_from_svg(get_data("../icons/circle-solid.svg"), QColor(color)))

class MatchsList(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        
        step1 = MatchItem("depth=1, x=2, y=13", "#ffca3a")
        self.addItem(step1)
        step2 = MatchItem("depth=1, x=2, y=13", "#1982c4")
        self.addItem(step2)
        step3 = MatchItem("depth=1, x=2, y=13", "#8ac926")
        self.addItem(step3)
        step4 = MatchItem("depth=1, x=2, y=13", "#ff595e")
        self.addItem(step4)
        step1.setSelected(True)
    
class MatchsWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)

        list = MatchsList()
        self.layout().addWidget(list)

        apply_button = QPushButton("Apply")
        self.layout().addWidget(apply_button)
        # self.layout().setSpacing(0)


class StepItem(QListWidgetItem):
    def __init__(self,  text="No text") -> None:
        super().__init__(text)
        # self.setIcon(QIcon(get_data("../icons/right-arrow.png")))


class StepsList(QListWidget):
    def __init__(self) -> None:
        super().__init__()
        
        step1 = StepItem("Step 1 (HH at depth=1, x=2, y=13)")
        self.addItem(step1)
        step2 = StepItem("Step 2 (P0 at depth=1, x=2, y=13)")
        self.addItem(step2)
        step3 = StepItem("Step 3 (Euler decomposition at depth=1, x=2, y=13)")
        self.addItem(step3)
        step4 = StepItem("Step 4 (HH at depth=1, x=2, y=13)")
        self.addItem(step4)
        step4.setSelected(True)

class StepsWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)

        steps = StepsList()
        self.layout().addWidget(steps)

        preview_button = QPushButton("Preview")
        self.layout().addWidget(preview_button)

        resume_button = QPushButton("Resume")
        self.layout().addWidget(resume_button)
    
class DerivWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)

        matchs = MatchsWidget()
        self.layout().addWidget(matchs)
        
        steps = StepsWidget()
        self.layout().addWidget(steps)