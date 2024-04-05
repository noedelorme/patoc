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
        self.setCursor(Qt.SizeHorCursor)
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


class GateItem(QGraphicsItemGroup):
    box_size = 30
    box_pen: QPen = QPen(QColor("black"), 2)
    font_size = 12
    font = QFont("Times", font_size)

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()
        self.scene = scene
        self.setZValue(1)

        self.edges = []
        
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
            self.input_pos.append((-self.box_size/2,0))
            self.output_pos.append((self.box_size/2,0))

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
    
    def updatePos(self) -> None:
        # utiliser cette methode dans le init pour pas dupliquer le code
        x,y = self.gate.pos
        if type(y) == int: y = [y]
        true_x = self.scene.grid.x(x)
        true_y_top = self.scene.grid.y(x,y[0])
        self.setPos(true_x,true_y_top)

    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)
        self.setZValue(2)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(e)
        for edge in self.edges: edge.updatePos()
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        self.setZValue(1)
        for item in self.scene.items():
            if isinstance(item, PlaceholderItem):
                if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
                    self.gate.pos = item.pos # problème quand la porte à plusieurs entrée
                    x,y = item.pos
                    if type(y) == int: y = [y]
                    true_x = self.scene.grid.x(x)
                    true_y = self.scene.grid.y(x,y[0])
                    self.setPos(true_x,true_y)
                    for edge in self.edges: edge.updatePos()
                    return
        x,y = self.gate.pos
        if type(y) == int: y = [y]
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y[0])
        self.setPos(true_x,true_y)
        for edge in self.edges: edge.updatePos()


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

        self.edges = []

        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        # self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        
        

        true_y_control = self.scene.grid.y(x,y[0])
        true_y_target = self.scene.grid.y(x,y[1])

        true_x = self.scene.grid.x(x)
        true_y = true_y_control

        self.controlItem = QGraphicsEllipseItem()
        self.controlItem.setPen(self.pen)
        self.controlItem.setBrush(self.color)
        self.controlItem.setRect(-self.control_radius,-self.control_radius,2*self.control_radius,2*self.control_radius)
        self.addToGroup(self.controlItem)

        # self.controlItem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        # def mousePressEventControl(self) -> None:
        #     print("OURA")
        # self.controlItem.mousePressEvent = mousePressEventControl
        # self.controlItem.setCursor(Qt.SizeVerCursor)

        

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

        self.targetItem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        
        self.setPos(true_x,true_y)

        self.input_pos = [
            (0,0),
            (-self.target_radius,0)
        ]
        self.output_pos = [
            (0,0),
            (self.target_radius,0)
        ]

    def updatePos(self) -> None:
        pass
        

class DividerItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()


class GathererItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()


class EdgeItem(QGraphicsLineItem):
    pen: QPen = QPen(QColor("black"), 2)

    def __init__(self, scene: Scene, s, t, wiring) -> None:
        super().__init__()
        self.scene = scene

        self.s = s
        self.t = t
        self.wiring = wiring

        x0,y0 = s.output_pos[wiring[0]]
        x1,y1 = t.input_pos[wiring[1]]
        x_s,y_s = s.gate.pos
        if type(y_s) == int: y_s = [y_s]
        true_x_s = self.scene.grid.x(x_s)
        true_y_s = self.scene.grid.y(x_s,y_s[wiring[0]])
        x_t,y_t = t.gate.pos
        if type(y_t) == int: y_t = [y_t]
        true_x_t = self.scene.grid.x(x_t)
        true_y_t = self.scene.grid.y(x_t,y_t[wiring[1]])

        self.setPos(true_x_s+x0,true_y_s+y0)
        dest_x = (true_x_t+x1)-(true_x_s+x0)
        dest_y = (true_y_t+y1)-(true_y_s+y0)
        self.setLine(0,0,dest_x,dest_y)
        self.setPen(self.pen)
    
    def updatePos(self) -> None:
        x0,y0 = self.s.output_pos[self.wiring[0]]
        x1,y1 = self.t.input_pos[self.wiring[1]]
        x_s,y_s = self.s.gate.pos
        if type(y_s) == int: y_s = [y_s]
        true_x_s = self.scene.grid.x(x_s)
        true_y_s = self.scene.grid.y(x_s,y_s[self.wiring[0]])
        x_t,y_t = self.t.gate.pos
        if type(y_t) == int: y_t = [y_t]
        true_x_t = self.scene.grid.x(x_t)
        true_y_t = self.scene.grid.y(x_t,y_t[self.wiring[1]])

        x_s,y_s = self.s.gate.pos
        if type(y_s) == int: y_s = [y_s]
        x_t,y_t = self.t.gate.pos
        if type(y_t) == int: y_t = [y_t]
        true_x_s = self.s.pos().x()
        true_y_s = self.s.pos().y()+self.scene.grid.y(x_s,y_s[self.wiring[0]])-self.scene.grid.y(x_s,y_s[0])
        true_x_t = self.t.pos().x()
        true_y_t = self.t.pos().y()+self.scene.grid.y(x_t,y_t[self.wiring[1]])-self.scene.grid.y(x_t,y_t[0])
        

        self.setPos(true_x_s+x0,true_y_s+y0)
        dest_x = (true_x_t+x1)-(true_x_s+x0)
        dest_y = (true_y_t+y1)-(true_y_s+y0)
        self.setLine(0,0,dest_x,dest_y)
        self.setPen(self.pen)