from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QFont, QIcon, QPainter, QPen, QPixmap

from ..utils import *


class MatchItem(QListWidgetItem):
    def __init__(self,  text="No text", color="green") -> None:
        super().__init__(text)
        self.color = color
        self.setIcon(QIcon_from_svg(get_data("icons/circle-solid.svg"), QColor(self.color)))

        self.is_visible = True

    def toggle_visibility(self) -> None:
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.setIcon(QIcon_from_svg(get_data("icons/circle-solid.svg"), QColor(self.color)))
        else:
            self.setIcon(QIcon_from_svg(get_data("icons/circle-empty.svg"), QColor(self.color)))

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

        self.itemDoubleClicked.connect(self.toggle_item_visibility)
    
    def toggle_item_visibility(self, item) -> None:
        item.toggle_visibility()
    
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