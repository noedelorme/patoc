from PySide6.QtWidgets import QMainWindow
from .scene import Scene, SceneView

class MainWindow(QMainWindow):
    """The main window of Patoc"""

    def __init__(self) -> None:
        super().__init__()

        scene = Scene()
        scene_view = SceneView(scene)
        self.setCentralWidget(scene_view)