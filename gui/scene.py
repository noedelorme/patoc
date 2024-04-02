from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QBrush, QColor, QPen, QRadialGradient, QGradient
from .items import GateItem, PlaceholderItem, EdgeItem
from engine.circuit import Gate

class Scene(QGraphicsScene):
    """Class for managing the graphical items"""
    
    def __init__(self) -> None:
        super().__init__()

        self.setBackgroundBrush(QColor("white"))
        self.drawPlaceholders()

        gate_item1 = GateItem(self, Gate(0, "A", pos=(0,0)))
        gate_item2 = GateItem(self, Gate(0, "B", pos=(3,0)))
        gate_item3 = GateItem(self, Gate(0, "C", pos=(4,1)))
        self.addItem(gate_item1)
        self.addItem(gate_item2)
        self.addItem(gate_item3)

        edge1 = EdgeItem(None,None)
        self.addItem(edge1)


    def drawPlaceholders(self) -> None:
        for i in range(10):
            for j in range(6):
                place = PlaceholderItem((i,j))
                self.addItem(place)
                

    



class SceneView(QGraphicsView):
    """Class for displaying the contents of a QGraphicsScene"""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        super().__init__(self.scene)