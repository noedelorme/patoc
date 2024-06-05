from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QTreeView, QGroupBox, QRadioButton, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QLabel
from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QFont


class RuleItem(QTreeWidgetItem):
    def __init__(self, text="No text") -> None:
        super().__init__(None, [text])

        self.equation = "secret"


class RulesTree(QTreeWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setColumnCount(1)
        self.headerItem().setHidden(True)

        root = self.invisibleRootItem()
        cat = RuleItem("Complete equational theory")
        root.addChild(cat)

        item1 = RuleItem("Euler decomposition")
        cat.addChild(item1)
        item2 = RuleItem("Control-Z")
        cat.addChild(item2)
        item3 = RuleItem("Hadamard cancellation")
        cat.addChild(item3)
        item4 = RuleItem("Control-P(2π)")
        cat.addChild(item4)
        item5 = RuleItem("P(0) introduction")
        cat.addChild(item5)
        item6 = RuleItem("Swap with Cnots")
        cat.addChild(item6)

        custom = RuleItem("Custom rules")
        root.addChild(custom)
        citem1 = RuleItem("Controls swapping")
        custom.addChild(citem1)
        citem2 = RuleItem("Phase gadget")
        custom.addChild(citem2)

        self.expandAll()

        self.itemDoubleClicked.connect(self.processItem)

    def processItem(self, item, column):
        print(item.equation)


class RulesWidget(QGroupBox):
    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)

        tree = RulesTree()
        self.layout().addWidget(tree)

        left2right = QRadioButton("Left to right")
        left2right.setChecked(True)
        left2right.toggled.connect(self.change_sens)
        self.layout().addWidget(left2right)
        right2left = QRadioButton("Right to left")
        self.layout().addWidget(right2left)

        show_button = QPushButton("Preview")
        match_button = QPushButton("Match")
        self.layout().addWidget(show_button)
        self.layout().addWidget(match_button)


    def change_sens(self) -> None:
        print("change sens", self.sender().isChecked())