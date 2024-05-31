from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction, QKeySequence

from .scene import Scene, SceneView
from .edit_panel import EditPanel

class MainWindow(QMainWindow):
    """The main window of Patoc"""

    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.setFixedSize(1200,600)
        menu_bar = self.menuBar()

        self.new_circuit_action = QAction("New circuit", self)
        self.new_circuit_action.triggered.connect(self.new_circuit)
        self.new_circuit_action.setShortcut(QKeySequence.StandardKey.New)
        self.open_circuit_action = QAction("Open circuit", self)
        self.open_circuit_action.triggered.connect(self.quit)
        self.open_circuit_action.setShortcut(QKeySequence.StandardKey.Open)
        self.new_rule_action = QAction("New rule", self)
        self.new_rule_action.triggered.connect(self.quit)
        self.new_set_of_rules_action = QAction("New set of rules", self)
        self.new_set_of_rules_action.triggered.connect(self.quit)
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.quit)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_as_action = QAction("Save as", self)
        self.save_as_action.triggered.connect(self.quit)
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.quit_action = QAction("Close", self)
        self.quit_action.triggered.connect(self.quit)
        self.quit_action.setShortcut(QKeySequence.StandardKey.Close)

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.new_circuit_action)
        file_menu.addAction(self.open_circuit_action)
        file_menu.addSeparator()
        file_menu.addAction(self.new_rule_action)
        file_menu.addAction(self.new_set_of_rules_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        self.github_action = QAction("Github repository", self)
        self.github_action.triggered.connect(self.quit)

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.github_action)

        edit_panel = EditPanel()
        self.setCentralWidget(edit_panel)
    
    def quit(self) -> None:
        self.app.quit()

    def new_circuit(self) -> None:
        pass