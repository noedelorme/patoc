from PySide6.QtWidgets import QWidget, QTreeView, QHBoxLayout, QVBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem

from PySide6.QtGui import QStandardItem, QStandardItemModel, QColor, QFont

class RuleItem(QTreeWidgetItem):
    def __init__(self, text="No text") -> None:
        super().__init__(None, [text])

        self.equation = "secret"

class RulesTreeWidget(QTreeWidget):
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

        self.expandAll()

        self.itemDoubleClicked.connect(self.processItem)

    def processItem(self, item, column):
        print(item.equation)

class RulesDisplayWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QVBoxLayout())

        show_button = QPushButton("show")
        sens_button = QPushButton("sens")
        self.layout().addWidget(show_button)
        self.layout().addWidget(sens_button)



class RulesWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        tree = RulesTreeWidget()
        display = RulesDisplayWidget()
        self.layout().addWidget(tree)
        self.layout().addWidget(display)

