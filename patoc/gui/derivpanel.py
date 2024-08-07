from PySide6.QtWidgets import QWidget, QGroupBox, QTreeView, QVBoxLayout, QHBoxLayout, QSplitter, QToolBar, QButtonGroup, QToolButton, QPushButton, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QFont
from PySide6.QtCore import Qt, QSize

from .rules import RulesWidget
from .scene import SceneWidget
from .steps import StepsWidget
from .matchs import MatchsWidget

from ..utils import *

class DerivToolbar(QToolBar):
    def __init__(self) -> None:
        super().__init__()
        icon_size = QSize(32,32)

        self.port_button = QToolButton()
        self.port_button.setText("Port")
        self.port_button.setCheckable(True)
        self.port_button.setToolTip("Decsription text todo")
        self.port_button.setIcon(QIcon_from_svg(get_data("icons/mtn.svg"), QColor("grey")))
        self.port_button.setIconSize(icon_size)
        self.port_button.clicked.connect(self.my_action)
        self.addWidget(self.port_button)

        self.move_button = QToolButton()
        self.move_button.setText("Move")
        self.move_button.setCheckable(True)
        self.move_button.setToolTip("Decsription text todo")
        self.move_button.setIcon(QIcon_from_svg(get_data("icons/mtn.svg"), QColor("blue")))
        self.move_button.setIconSize(icon_size)
        self.move_button.clicked.connect(self.my_action)
        self.addWidget(self.move_button)
    
    def my_action(self) -> None:
        pass


class DerivPanel(QWidget):
    """The edit panel for applying axioms"""

    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QVBoxLayout())
        # self.layout().setSpacing(0)
        # self.layout().setContentsMargins(5,5,5,5)

        self.splitter = QSplitter()
        self.splitter.setChildrenCollapsible(False)
        self.layout().addWidget(self.splitter)

        rules_sidebar = RulesWidget()
        rules_sidebar.setMinimumWidth(200)
        self.splitter.addWidget(rules_sidebar)

        scene = SceneWidget()
        scene.setMinimumWidth(200)
        self.splitter.addWidget(scene)

        matchs_steps_sidebar = QSplitter()
        matchs_steps_sidebar.setOrientation(Qt.Vertical)
        matchs_steps_sidebar.setMinimumWidth(200)
        matchs_steps_sidebar.setChildrenCollapsible(False)
        matchs_widget = MatchsWidget()
        steps_widget = StepsWidget()
        matchs_widget.setMinimumHeight(200)
        steps_widget.setMinimumHeight(200)
        matchs_steps_sidebar.addWidget(matchs_widget)
        matchs_steps_sidebar.addWidget(steps_widget)
        self.splitter.addWidget(matchs_steps_sidebar)