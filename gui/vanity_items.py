from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QColor, QPen
from engine.circuit import Gate

if TYPE_CHECKING:
    from .scene import Scene

class PlaceholderItem(QGraphicsEllipseItem):
    placeholder_size = 8

    def __init__(self, scene, pos) -> None:
        super().__init__()
        self.scene = scene
        self.pos = pos

        self.setZValue(0)
        self.setPen(QPen(QColor(0, 0, 0, 0), 1))
        self.setBrush(QColor(0, 0, 0, 40))
        self.setRect(-self.placeholder_size/2,-self.placeholder_size/2,self.placeholder_size,self.placeholder_size)

        x,y = pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y)
        self.setPos(true_x,true_y)
    
    def updatePos(self) -> None:
        x,y = self.pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y)
        self.setPos(true_x,true_y)

class GridLineItem(QGraphicsLineItem):
    pen = QPen(QColor(0, 0, 0, 40), 1)
    pen.setDashPattern((2,8))

    def __init__(self, scene, i) -> None:
        super().__init__()
        self.scene = scene
        self.i = i

        self.setZValue(0)
        self.setCursor(Qt.SizeVerCursor)
        self.setLine(0,0,0,self.scene.height())
        self.setPen(self.pen)
        self.setPos(self.scene.grid.x(i),self.scene.sceneRect().y())

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
    
    def updatePos(self) -> None:
        self.setPos(self.scene.grid.x(self.i),self.scene.sceneRect().y())
    
    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.setPos(e.scenePos().x(),self.scene.sceneRect().y())

    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        old_pos = self.scene.grid.true_x[self.i]
        new_pos = self.pos().x()
        delta = new_pos-old_pos

        for i in range(self.i, self.scene.grid.nb_cols):
            self.scene.grid.true_x[i] += delta
        
        self.scene.updatePos()


class BoundItem(QGraphicsRectItem):
    bound_size = 8

    def __init__(self, scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.gate = gate

        self.edges = []

        self.setCursor(Qt.SizeVerCursor)

        self.setBrush(QColor("black"))
        self.setRect(-self.bound_size/2,-self.bound_size/2,self.bound_size,self.bound_size)

        x,y = gate.pos
        if type(y) == int: y = [y]
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y[0])
        self.setPos(true_x,true_y)

        self.input_pos = [(0,0)]
        self.output_pos = [(0,0)]
    
    def updatePos(self) -> None:
        x,y = self.gate.pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y)
        self.setPos(true_x,true_y)
        for edge in self.edges: edge.updatePos()