from PySide6.QtWidgets import QWidget, QTreeView, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QFont

from .rules_widget import RulesWidget
from .scene import SceneWidget
from .deriv_widget import DerivWidget


class EditPanel(QWidget):
    """The edit panel for applying axioms"""

    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QHBoxLayout())
        # self.layout().setContentsMargins(5,5,5,5)

        rules_sidebar = RulesWidget()
        rules_sidebar.setFixedWidth(250)
        self.layout().addWidget(rules_sidebar)

        scene = SceneWidget()
        self.layout().addWidget(scene)

        deriv_sidebar = DerivWidget()
        deriv_sidebar.setFixedWidth(250)
        self.layout().addWidget(deriv_sidebar)
    
    def itemDoubleClickEvent(self, val):
        print(val.parent())


        