from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from .items import GateItem
from engine.circuit import Gate

class Scene(QGraphicsScene):
    """Class for managing the graphical items"""
    
    def __init__(self) -> None:
        super().__init__()

        gate = Gate(0, "H")

        gate_item = GateItem(self, gate)
        self.addItem(gate_item)



class SceneView(QGraphicsView):
    """Class for displaying the contents of a QGraphicsScene"""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        super().__init__(self.scene)