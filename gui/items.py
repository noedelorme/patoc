from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainterPath
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
        placeholder_padding = GateItem.box_size/2-self.placeholder_size/2
        self.setRect(placeholder_padding,placeholder_padding,self.placeholder_size,self.placeholder_size)

        x,y = pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y)
        self.setPos(true_x,true_y)

class BoundItem(QGraphicsRectItem):
    bound_size = 6

    def __init__(self, scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.gate = gate

        self.setBrush(QColor("black"))
        bound_padding = GateItem.box_size/2-self.bound_size/2
        self.setRect(bound_padding,bound_padding,self.bound_size,self.bound_size)

        x,y = gate.pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y)
        self.setPos(true_x,true_y)

        self.input_pos = [(true_x+bound_padding,true_y+bound_padding+self.bound_size/2)]
        self.output_pos = [(true_x+bound_padding+self.bound_size,true_y+bound_padding+self.bound_size/2)]

class GateItem(QGraphicsItemGroup):
    box_size = 30
    box_pen: QPen = QPen(QColor("black"), 2)
    font = QFont("Times", 12)

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.setZValue(1)
        
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
        if type(y) == int: y = [y]
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y[0])
        self.setPos(true_x,true_y)
        self.input_pos = [(true_x,true_y+self.box_size/2)]
        self.output_pos = [(true_x+self.box_size,true_y+self.box_size/2)]

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


class ConsecutiveMultiGateItem(QGraphicsItemGroup):
    def __init__(self) -> None:
        super().__init__()


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
        control_padding = GateItem.box_size/2-self.control_radius
        control_size = 2*self.control_radius
        self.controlItem.setRect(control_padding,control_padding,control_size,control_size)
        self.addToGroup(self.controlItem)

        self.targetItem = QGraphicsPathItem()
        self.targetItem.setPen(self.pen)
        path = QPainterPath()
        target_padding = GateItem.box_size/2-self.target_radius
        target_size = 2*self.target_radius
        target_relative_y = true_y_target-true_y_control
        path.addEllipse(target_padding,target_relative_y+target_padding,target_size,target_size)
        path.moveTo(GateItem.box_size/2,GateItem.box_size/2)
        path.lineTo(GateItem.box_size/2,target_padding+target_relative_y+target_size) # vertical line
        path.moveTo(GateItem.box_size/2-self.target_radius,target_relative_y+GateItem.box_size/2)
        path.lineTo(GateItem.box_size/2+self.target_radius,target_relative_y+GateItem.box_size/2)
        self.targetItem.setPath(path)
        self.addToGroup(self.targetItem)
        
        self.setPos(true_x,true_y)

        self.input_pos = [
            (true_x+control_padding,true_y_control+control_padding+control_size/2),
            (true_x+target_padding,true_y_target+target_padding+target_size/2)
        ]
        self.output_pos = [
            (true_x+control_padding+control_size,true_y_control+control_padding+control_size/2),
            (true_x+target_padding+target_size,true_y_target+target_padding+target_size/2)
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