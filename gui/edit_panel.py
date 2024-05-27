from PySide6.QtWidgets import QWidget, QTreeView, QHBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QFont

from .rules_widget import RulesWidget, RulesTreeWidget
from .scene import Scene, SceneView
from .steps_widget import StepsWidget


class EditPanel(QWidget):
    """The edit panel for applying axioms"""

    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QHBoxLayout())
        # self.layout().setContentsMargins(0, 0, 0, 0)

        rules_sidebar = RulesWidget()
        rules_sidebar.setFixedWidth(200)
        self.layout().addWidget(rules_sidebar)

        scene = Scene()
        scene_view = SceneView(scene)
        self.layout().addWidget(scene_view)

        steps_sidebar = StepsWidget()
        steps_sidebar.setFixedWidth(200)
        self.layout().addWidget(steps_sidebar)
    
    def itemDoubleClickEvent(self, val):
        print(val.parent())


        