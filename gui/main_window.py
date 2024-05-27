from PySide6.QtWidgets import QMainWindow
from .scene import Scene, SceneView
from .edit_panel import EditPanel

class MainWindow(QMainWindow):
    """The main window of Patoc"""

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(1200,600)

        # scene = Scene()
        # scene_view = SceneView(scene)
        # self.setCentralWidget(scene_view)

        edit_panel = EditPanel()
        self.setCentralWidget(edit_panel)