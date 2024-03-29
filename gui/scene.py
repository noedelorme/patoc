from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtGui import QBrush, QColor, QPen, QRadialGradient, QGradient
from .items import GateItem
from engine.circuit import Gate

class Scene(QGraphicsScene):
    """Class for managing the graphical items"""
    
    def __init__(self) -> None:
        super().__init__()

        self.setBackgroundBrush(QColor(255, 255, 255, 255))

        gate_item1 = GateItem(self, Gate(0, "H"))
        gate_item2 = GateItem(self, Gate(0, "H"))
        self.addItem(gate_item1)
        self.addItem(gate_item2)

        gate_item1.setPos(0,0)
        gate_item1.setPos(500,100)



class SceneView(QGraphicsView):
    """Class for displaying the contents of a QGraphicsScene"""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        super().__init__(self.scene)