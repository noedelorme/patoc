from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainterPath
from engine.circuit import Gate

if TYPE_CHECKING:
    from .scene import Scene

class GateItem(QGraphicsItemGroup):
    box_size = 30
    box_pen: QPen = QPen(QColor("black"), 2)
    font = QFont("Times", 12)

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        
        self.gate = gate
        self.box = QGraphicsRectItem()
        self.text = QGraphicsTextItem()
        self.text.setPlainText(self.gate.type)
        self.text.setDefaultTextColor(QColor("black"))
        self.text.setFont(self.font)
        self.text.setPos(5,5)
        self.box.setPen(self.box_pen)
        self.box.setBrush(QColor("white"))
        self.box.setRect(0,0,self.box_size,self.box_size)

        self.addToGroup(self.box)
        self.addToGroup(self.text)

        x,y = self.gate.pos
        self.setPos(x*50,y*50)
        self.input_pos = ()

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)
        self.setZValue(1)
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        self.setZValue(0)
        for item in self.scene.items():
            if isinstance(item, PlaceholderItem):
                if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
                    self.gate.pos = (item.x,item.y)
                    self.setPos(item.x*50,item.y*50)
                    return
        x,y = self.gate.pos
        self.setPos(x*50,y*50)
        
class PlaceholderItem(QGraphicsPathItem):
    box_pen: QPen = QPen(QColor("black"), 2)
    font = QFont("Times", 12)

    def __init__(self, pos) -> None:
        super().__init__()

        self.x,self.y = pos
    
        path = QPainterPath()
        # path.addRect(0,0,30,30)
        path.addEllipse(12,12,5,5)
        self.setPen(QPen(QColor(0, 0, 0, 0), 1))
        self.setBrush(QColor(0, 0, 0, 40))
        self.setPath(path)
        self.setPos(self.x*50,self.y*50)


class MultiGateItem(QGraphicsItemGroup):
    def __init__(self) -> None:
        super().__init__()


class CnotItem(QGraphicsItemGroup):
    def __init__(self) -> None:
        super().__init__()

        self.controlItem = QGraphicsEllipseItem()
        self.targetItem = QGraphicsPathItem()


class DividerItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()


class GathererItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()


class EdgeItem(QGraphicsLineItem):
    pen: QPen = QPen(QColor("black"), 2)

    def __init__(self, s, t) -> None:
        super().__init__()

        self.setLine(2*50,2*50,4*50,2*50)
        self.setPen(self.pen)