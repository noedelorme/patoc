from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainterPath, QCursor
from engine.circuit import Gate

if TYPE_CHECKING:
    from .scene import Scene

class PlaceholderItem(QGraphicsEllipseItem):
    placeholder_size = 8

    def __init__(self, scene, pos) -> None:
        super().__init__()
        self.scene = scene
        self.pos = pos
    
        self.setPen(QPen(QColor(0, 0, 0, 0), 1))
        self.setBrush(QColor(0, 0, 0, 40))
        self.setRect(-self.placeholder_size/2,-self.placeholder_size/2,self.placeholder_size,self.placeholder_size)

        x,y = pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y)
        self.setPos(true_x,true_y)

class BoundItem(QGraphicsRectItem):
    bound_size = 8

    def __init__(self, scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.gate = gate

        self.setCursor(Qt.SizeVerCursor)

        self.setBrush(QColor("black"))
        self.setRect(-self.bound_size/2,-self.bound_size/2,self.bound_size,self.bound_size)

        x,y = gate.pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y)
        self.setPos(true_x,true_y)

        self.input_pos = [(true_x,true_y)]
        self.output_pos = [(true_x,true_y)]

class GateItem(QGraphicsItemGroup):
    box_size = 30
    box_pen: QPen = QPen(QColor("black"), 2)
    font_size = 12
    font = QFont("Times", font_size)

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.setZValue(1)
        
        self.gate = gate
        x,y = self.gate.pos
        if type(y) == int: y = [y]
        true_x = self.scene.grid.x(x)
        true_y_top = self.scene.grid.y(x,y[0])
        true_y_bottom = self.scene.grid.y(x,y[-1])

        self.box = QGraphicsRectItem()
        self.text = QGraphicsTextItem()
        self.text.setPlainText(self.gate.type)
        self.text.setDefaultTextColor(QColor("black"))
        self.text.setFont(self.font)
        self.text.setPos(-self.font_size+2,-self.font_size+2+(true_y_bottom-true_y_top)/2)
        self.box.setPen(self.box_pen)
        self.box.setBrush(QColor("white"))
        self.box.setRect(-self.box_size/2,-self.box_size/2,self.box_size,true_y_bottom-true_y_top+self.box_size)
        self.addToGroup(self.box)
        self.addToGroup(self.text)
        self.setPos(true_x,true_y_top)


        self.input_pos = []
        self.output_pos = []

        for i in range(self.gate.dom):
            true_y = self.scene.grid.y(x,y[i])
            self.input_pos.append((true_x-self.box_size/2,true_y))
            self.output_pos.append((true_x+self.box_size/2,true_y))

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)
        self.setZValue(2)
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        self.setZValue(1)
        for item in self.scene.items():
            if isinstance(item, PlaceholderItem):
                if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
                    self.gate.pos = item.pos
                    x,y = item.pos
                    if type(y) == int: y = [y]
                    true_x = self.scene.grid.x(x)
                    true_y = self.scene.grid.y(x,y[0])
                    self.setPos(true_x,true_y)
                    return
        x,y = self.gate.pos
        if type(y) == int: y = [y]
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y[0])
        self.setPos(true_x,true_y)


class SparseGateItem(QGraphicsItemGroup):
    box_size = 30
    box_pen: QPen = QPen(QColor("black"), 2)
    font = QFont("Times", 12)

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.setZValue(1)



class CnotItem(QGraphicsItemGroup):
    pen = QPen(QColor("black"), 2)
    color = QColor("black")
    control_radius = 4
    target_radius = 10

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.gate = gate
        x,y = self.gate.pos
        

        true_y_control = self.scene.grid.y(x,y[0])
        true_y_target = self.scene.grid.y(x,y[1])

        true_x = self.scene.grid.x(x)
        true_y = true_y_control

        self.controlItem = QGraphicsEllipseItem()
        self.controlItem.setPen(self.pen)
        self.controlItem.setBrush(self.color)
        self.controlItem.setRect(-self.control_radius,-self.control_radius,2*self.control_radius,2*self.control_radius)
        self.addToGroup(self.controlItem)

        self.targetItem = QGraphicsPathItem()
        self.targetItem.setPen(self.pen)
        path = QPainterPath()
        target_padding = GateItem.box_size/2-self.target_radius
        target_size = 2*self.target_radius
        target_relative_y = true_y_target-true_y_control
        path.addEllipse(-self.target_radius,target_relative_y-self.target_radius,target_size,target_size)
        path.moveTo(0,0)
        path.lineTo(0,target_relative_y+self.target_radius) # vertical line
        path.moveTo(-self.target_radius,target_relative_y)
        path.lineTo(self.target_radius,target_relative_y)
        self.targetItem.setPath(path)
        self.addToGroup(self.targetItem)
        
        self.setPos(true_x,true_y)

        self.input_pos = [
            (true_x,true_y_control),
            (true_x-self.target_radius,true_y_target)
        ]
        self.output_pos = [
            (true_x,true_y_control),
            (true_x+self.target_radius,true_y_target)
        ]
        

class DividerItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()


class GathererItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()


class EdgeItem(QGraphicsLineItem):
    pen: QPen = QPen(QColor("black"), 2)

    def __init__(self, s, t, wiring) -> None:
        super().__init__()

        self.s = s
        self.t = t
        self.wiring = wiring

        true_x0,true_y0 = s.output_pos[wiring[0]]
        true_x1,true_y1 = t.input_pos[wiring[1]]
        self.setLine(true_x0,true_y0,true_x1,true_y1)
        self.setPen(self.pen)