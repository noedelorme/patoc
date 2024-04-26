from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPointF, QSizeF, QRectF
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainterPath, QCursor, QPolygonF
from engine.circuit import Gate

from .utils import *
import math as math

if TYPE_CHECKING:
    from .scene import Scene


class BoundItem(QGraphicsItemGroup):
    pen = QPen(QColor("blue"), 2)
    color = QColor("blue")
    radius = 3

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.gate = gate
        self.setZValue(3)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.edges = []
        self.inputs = [] if self.gate.type == "in" else [self]
        self.outputs = [self] if self.gate.type == "in" else []

        self.bullet = QGraphicsEllipseItem()
        self.bullet.setCursor(Qt.OpenHandCursor)
        self.bullet.setPen(self.pen)
        self.bullet.setBrush(self.color)
        self.bullet.setRect(-self.radius,-self.radius,2*self.radius,2*self.radius)
        self.addToGroup(self.bullet)
        self.update()

        self.scene.addItem(self)
    
    def update(self) -> None:
        self.x = self.gate.pos[0]
        self.y = self.gate.pos[2][0] if self.gate.type == "in" else self.gate.pos[1][0]
        self.setPos(pos(self.x),pos(self.y))
        for edge in self.edges: edge.update()

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.x = invpos(e.scenePos().x()-e.buttonDownPos(Qt.LeftButton).x())
        self.y = invpos(e.scenePos().y()-e.buttonDownPos(Qt.LeftButton).y())
        input_ys = [] if self.gate.type == "in" else [self.y]
        output_ys = [self.y] if self.gate.type == "in" else []
        self.gate.pos = (self.x, input_ys, output_ys)
        self.update()
    
    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.bullet.setCursor(Qt.ClosedHandCursor)
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.bullet.setCursor(Qt.OpenHandCursor)


class BoxItem(QGraphicsItemGroup):
    box_pen: QPen = QPen(QColor("black"), 2)
    font_size = 12
    font = QFont("Helvetica", font_size)
    font.setBold(True)

    def __init__(self, group: GateGroup) -> None:
        super().__init__()
        self.group = group
        self.gate = self.group.gate
        self.setZValue(2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        self.box = QGraphicsRectItem()
        self.box.setCursor(Qt.OpenHandCursor)
        self.box.setPen(self.box_pen)
        self.box.setBrush(QColor(240,240,240))
        self.addToGroup(self.box)

        self.text = QGraphicsTextItem()
        self.text.setPlainText(self.group.target_type)
        self.text.setDefaultTextColor(QColor("black"))
        
        self.text.setFont(self.font)
        self.addToGroup(self.text)

        self.update()
    
    def update(self) -> None:
        x,yin,yout = self.gate.pos
        min_y= min(yin[self.group.nb_controls:]+yout[self.group.nb_controls:])
        max_y = max(yin[self.group.nb_controls:]+yout[self.group.nb_controls:])
        self.x = x
        self.y = min_y-1
        height = pos(max_y+1)-pos(min_y-1)
        self.box.setRect(0,0,pos(self.group.box_size),height)
        self.setPos(pos(self.x),pos(self.y))
        self.text.setPos(pos(self.group.box_size)/2-10,height/2-10)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        old_x, old_y = self.x, self.y
        self.x = invpos(e.scenePos().x()-e.buttonDownPos(Qt.LeftButton).x())
        self.y = invpos(e.scenePos().y()-e.buttonDownPos(Qt.LeftButton).y())
        delta_x = self.x-old_x
        delta_y = self.y-old_y

        input_ys,output_ys = [],[]
        for control in self.group.controls:
            control.x += delta_x
            control.y += delta_y
            input_ys.append(control.y)
            output_ys.append(control.y)
        for input in self.group.inputs:
            input.x += delta_x
            input.y += delta_y
            input_ys.append(input.y)
        for output in self.group.outputs:
            output.x += delta_x
            output.y += delta_y
            output_ys.append(output.y)
        self.gate.pos = (self.x, input_ys, output_ys)
        
        self.group.update()
    
    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.box.setCursor(Qt.ClosedHandCursor)
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.box.setCursor(Qt.OpenHandCursor)

class PortItem(QGraphicsRectItem):
    port_size = 5
    port_pen = QPen(QColor("blue"), 1)
    port_brush = QBrush(QColor("blue"))

    def __init__(self, group: GateGroup, type: str, id: int) -> None:
        super().__init__()
        self.group = group
        self.gate = self.group.gate
        self.type = type
        self.id = id
        self.setCursor(Qt.SizeVerCursor)
        self.setZValue(3)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        type_id = 1 if type=="in" else 2
        self.x = self.gate.pos[0]+self.group.input_rel_x if self.type == "in" else self.gate.pos[0]+self.group.output_rel_x
        self.y = self.gate.pos[type_id][id]

        self.setPen(self.port_pen)
        self.setBrush(self.port_brush)
        self.setRect(-self.port_size/2,-self.port_size/2,self.port_size,self.port_size)

        self.update()
    
    def update(self) -> None:
        self.setPos(pos(self.x),pos(self.y))
    
    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.y = invpos(e.scenePos().y())
        x, input_ys, output_ys = self.gate.pos
        if self.type == "in": input_ys[self.id] = self.y
        if self.type == "out": output_ys[self.id] = self.y
        self.gate.pos = (x, input_ys, output_ys)
        self.group.update()


class ControlItem(QGraphicsEllipseItem):
    radius = 5
    control_pen = QPen(QColor("black"), 1)
    control_brush = QBrush(QColor("black"))

    def __init__(self, group: GateGroup, id: int) -> None:
        super().__init__()
        self.group = group
        self.gate = self.group.gate
        self.id = id
        self.setZValue(2)
        self.setCursor(Qt.SizeVerCursor)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.x = self.gate.pos[0]+int(self.group.box_size/2)
        self.y = self.gate.pos[1][id]

        self.setPen(self.control_pen)
        self.setBrush(self.control_brush)
        self.setRect(-self.radius,-self.radius,2*self.radius,2*self.radius)

        self.update()
    
    def update(self) -> None:
        self.setPos(pos(self.x),pos(self.y))
    
    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.y = invpos(e.scenePos().y())
        x, input_ys, output_ys = self.gate.pos
        input_ys[self.id] = self.y
        output_ys[self.id] = self.y
        self.gate.pos = (x, input_ys, output_ys)
        self.group.update()


class GateGroup:
    default_box_size = 2
    box_pen: QPen = QPen(QColor("black"), 2)
    font_size = 12
    font = QFont("Times", font_size)
    port_size = 5
    port_pen = QPen(QColor("blue"), 1)
    port_brush = QBrush(QColor("blue"))
    control_pen: QPen = QPen(QColor("black"), 2)
    input_rel_x = 0
    output_rel_x = default_box_size

    def __init__(self, scene: Scene, gate: Gate, size=None) -> None:
        self.scene = scene
        self.gate = gate
        self.edges = []

        self.nb_controls, self.target_type = type_parse(self.gate.type)

        self.box_size = self.default_box_size if size==None else size
        self.box = BoxItem(self)
        self.scene.addItem(self.box)

        self.controls,self.inputs,self.outputs = [],[],[]
        for i in range(self.nb_controls):
            control = ControlItem(self, i)
            self.controls.append(control)
            self.scene.addItem(control)
        for i in range(self.nb_controls,self.gate.dom):
            port = PortItem(self, "in", i)
            self.inputs.append(port)
            self.scene.addItem(port)
        for i in range(self.nb_controls,self.gate.cod):
            port = PortItem(self, "out", i)
            self.outputs.append(port)
            self.scene.addItem(port)

        self.line = QGraphicsLineItem()
        self.line.setPen(self.control_pen)
        self.scene.addItem(self.line)

        self.update()
        
    def update(self) -> None:
        x,yin,yout = self.gate.pos
        min_y,max_y = min(yin+yout),max(yin+yout)
        self.line.setPos(pos(x+int(self.box_size/2)),pos(min_y))
        self.line.setLine(0,0,0,pos(max_y-min_y))
        for control in self.controls: control.update()
        for input in self.inputs: input.update()
        for output in self.outputs: output.update()
        self.box.update()
        for edge in self.edges: edge.update()

class DividerItem(QGraphicsPathItem):
    divider_size = 20

    def __init__(self, group: DividerGroup) -> None:
        super().__init__()
        self.group = group
        self.gate = self.group.gate
        self.setZValue(2)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setCursor(Qt.OpenHandCursor)

        self.setPen(QPen(QColor("black"), 2))
        self.setBrush(QColor(240,240,240))

        path = QPainterPath()
        self.p1 = QPointF(0, 0)
        self.p2 = QPointF(self.divider_size, -self.divider_size*2/math.sqrt(3)/2)
        self.p3 = QPointF(self.divider_size, self.divider_size*2/math.sqrt(3)/2)
        poly = QPolygonF([self.p1,self.p2,self.p3,self.p1])
        path.addPolygon(poly)
        self.setPath(path)

        self.update()
    
    def update(self) -> None:
        self.x = self.gate.pos[0]
        self.y = self.gate.pos[1][0]
        self.setPos(pos(self.x),pos(self.y))

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        old_x, old_y = self.x, self.y
        self.x = invpos(e.scenePos().x()-e.buttonDownPos(Qt.LeftButton).x())
        self.y = invpos(e.scenePos().y()-e.buttonDownPos(Qt.LeftButton).y())
        delta_x = self.x-old_x
        delta_y = self.y-old_y

        input_ys,output_ys = [],[]
        for input in self.group.inputs:
            input.x += delta_x
            input.y += delta_y
            input_ys.append(input.y)
        for output in self.group.outputs:
            output.x += delta_x
            output.y += delta_y
            output_ys.append(output.y)
        self.gate.pos = (self.x, input_ys, output_ys)
        
        self.group.update()
    
    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.setCursor(Qt.ClosedHandCursor)
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.setCursor(Qt.OpenHandCursor)
    

class DividerGroup:
    input_rel_x = -1
    output_rel_x = 2

    def __init__(self, scene: Scene, gate: Gate, size=None) -> None:
        self.scene = scene
        self.gate = gate
        self.edges = []

        self.divider = DividerItem(self)
        self.scene.addItem(self.divider)

        self.inputs,self.outputs = [],[]
        for i in range(self.gate.dom):
            port = PortItem(self, "in", i)
            self.inputs.append(port)
            self.scene.addItem(port)
        for i in range(self.gate.cod):
            port = PortItem(self, "out", i)
            self.outputs.append(port)
            self.scene.addItem(port)

        self.lines = QGraphicsPathItem()
        self.lines.setPen(QPen(QColor("black"), 2))
        self.scene.addItem(self.lines)

        self.update()
        
    def update(self) -> None:
        path = QPainterPath()
        # input line
        path.moveTo(self.divider.p1)
        input_x = self.gate.pos[0]+self.input_rel_x - self.divider.x
        input_y = self.gate.pos[1][0] - self.divider.y
        path.cubicTo(pos(input_x), pos(input_y), pos(input_x), pos(input_y), pos(input_x), pos(input_y))
        # first output line
        path.moveTo(self.divider.p2)
        output_x = self.gate.pos[0]+self.output_rel_x - self.divider.x
        output_y = self.gate.pos[2][0] - self.divider.y
        path.cubicTo(pos(output_x-2/3), pos(output_y), pos(output_x), pos(output_y), pos(output_x), pos(output_y))
        # second output line
        path.moveTo(self.divider.p3)
        output_x = self.gate.pos[0]+self.output_rel_x - self.divider.x
        output_y = self.gate.pos[2][1] - self.divider.y
        path.cubicTo(pos(output_x-2/3), pos(output_y), pos(output_x), pos(output_y), pos(output_x), pos(output_y))
        self.lines.setPos(pos(self.divider.x),pos(self.divider.y))
        self.lines.setPath(path)

        for input in self.inputs: input.update()
        for output in self.outputs: output.update()
        self.divider.update()
        for edge in self.edges: edge.update()