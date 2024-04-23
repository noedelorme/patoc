from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPointF, QSizeF, QRectF
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainterPath, QCursor
from engine.circuit import Gate

from .utils import *

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

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.bullet.setCursor(Qt.ClosedHandCursor)
        new_x = invpos(e.scenePos().x()-e.buttonDownPos(Qt.LeftButton).x())
        new_y = invpos(e.scenePos().y()-e.buttonDownPos(Qt.LeftButton).y())
        self.setPos(pos(new_x),pos(new_y))
        for edge in self.edges: edge.update()
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        self.bullet.setCursor(Qt.OpenHandCursor)
        self.x, self.y = invpos(self.pos().x()), invpos(self.pos().y())
        input_ys = [] if self.gate.type == "in" else [self.y]
        output_ys = [self.y] if self.gate.type == "in" else []
        self.gate.pos = (self.x, input_ys, output_ys)
        self.update()


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
        self.x = self.gate.pos[0] if self.type == "in" else self.gate.pos[0]+self.group.box_size
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
            # self.inputs.append(control)
            # self.outputs.append(control)
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
































# class GateItem(QGraphicsItemGroup):
#     box_size = 30
#     box_pen: QPen = QPen(QColor("black"), 2)
#     font_size = 12
#     font = QFont("Times", font_size)

#     def __init__(self, scene: Scene, gate: Gate) -> None:
#         super().__init__()

#         self.scene = scene
#         self.gate = gate
#         self.setZValue(1)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
#         self.edges = []
        
#         x,y = self.gate.pos
#         if type(y) == int: y = [y]
#         true_y_top = self.scene.grid.y(x,y[0])
#         true_y_bottom = self.scene.grid.y(x,y[-1])

#         self.box = QGraphicsRectItem()
#         self.text = QGraphicsTextItem()
#         self.text.setPlainText(self.gate.type)
#         self.text.setDefaultTextColor(QColor("black"))
#         self.text.setFont(self.font)
#         self.text.setPos(-self.font_size+2,-self.font_size+2+(true_y_bottom-true_y_top)/2)
#         self.box.setPen(self.box_pen)
#         self.box.setBrush(QColor("white"))
#         self.box.setRect(-self.box_size/2,-self.box_size/2,self.box_size,true_y_bottom-true_y_top+self.box_size)
#         self.addToGroup(self.box)
#         self.addToGroup(self.text)

#         self.updatePos()

#         self.input_pos = []
#         self.output_pos = []

#         for i in range(self.gate.dom):
#             self.input_pos.append((-self.box_size/2,0))
#             self.output_pos.append((self.box_size/2,0))
    
#     def updatePos(self) -> None:
#         x,y = self.gate.pos
#         if type(y) == int: y = [y]
#         true_x = self.scene.grid.x(x)
#         true_y_top = self.scene.grid.y(x,y[0])
#         self.setPos(true_x,true_y_top)
    
#     def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mousePressEvent(e)
#         self.setZValue(2)

#     def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mouseMoveEvent(e)
#         for edge in self.edges: edge.updatePos()
    
#     def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mouseReleaseEvent(e)
#         self.setZValue(1)
#         for item in self.scene.placeholders:
#             if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
#                 y_item = item.pos[1]
#                 if type(y_item)==int:y_item=[y_item]
#                 self.gate.pos = (item.pos[0],[y_item[0]+i for i in range(self.gate.dom)])

#                 self.updatePos()

#                 for edge in self.edges: edge.updatePos()
#                 return
#         self.updatePos()
#         for edge in self.edges: edge.updatePos()

# class ControlItem(QGraphicsItemGroup):
#     pen = QPen(QColor("black"), 2)
#     color = QColor("black")
#     radius = 4

#     def __init__(self, scene: Scene, gate: Gate) -> None:
#         super().__init__()

#         self.scene = scene
#         self.gate = gate
#         self.setZValue(1)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
#         self.edges = []
    
#         self.bullet = QGraphicsEllipseItem()
#         self.bullet.setPen(self.pen)
#         self.bullet.setBrush(self.color)
#         self.bullet.setRect(-self.radius,-self.radius,2*self.radius,2*self.radius)
#         self.addToGroup(self.bullet)

#         self.updatePos()

#         self.input_pos = [(-self.radius,0)]
#         self.output_pos = [(self.radius,0)]
    
#     def updatePos(self) -> None:
#         x,y = self.gate.pos
#         true_x = self.scene.grid.x(x)
#         true_y = self.scene.grid.y(x,y[0])
#         self.setPos(true_x,true_y)
    
#     def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mousePressEvent(e)
#         self.setZValue(2)

#     def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mouseMoveEvent(e)
#         for edge in self.edges: edge.updatePos()
    
#     def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mouseReleaseEvent(e)
#         self.setZValue(1)
#         for item in self.scene.placeholders:
#             if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
#                 y_item = item.pos[1]
#                 if type(y_item)==int:y_item=[y_item]
#                 self.gate.pos = (item.pos[0],[y_item[0]+i for i in range(self.gate.dom)])

#                 # x,y = item.pos
#                 # if type(y) == int: y = [y]
#                 # true_x = self.scene.grid.x(x)
#                 # true_y = self.scene.grid.y(x,y[0])
#                 # self.setPos(true_x,true_y)
#                 self.updatePos()

#                 for edge in self.edges: edge.updatePos()
#                 return
#         # x,y = self.gate.pos
#         # if type(y) == int: y = [y]
#         # true_x = self.scene.grid.x(x)
#         # true_y = self.scene.grid.y(x,y[0])
#         # self.setPos(true_x,true_y)
#         self.updatePos()
#         for edge in self.edges: edge.updatePos()


# class NotItem(QGraphicsItemGroup):
#     pen = QPen(QColor("black"), 2)
#     color = QColor("black")
#     radius = 10

#     def __init__(self, scene: Scene, gate: Gate) -> None:
#         super().__init__()

#         self.scene = scene
#         self.gate = gate
#         self.setZValue(1)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
#         self.edges = []
    
#         self.oplus = QGraphicsPathItem()
#         self.oplus.setPen(self.pen)
#         path = QPainterPath()
#         path.addEllipse(-self.radius,-self.radius,2*self.radius,2*self.radius)
#         path.moveTo(-self.radius,0)
#         path.lineTo(self.radius,0)
#         path.moveTo(0,-self.radius)
#         path.lineTo(0,self.radius)
#         self.oplus.setPath(path)
#         self.addToGroup(self.oplus)

#         self.updatePos()

#         self.input_pos = [(-self.radius,0)]
#         self.output_pos = [(self.radius,0)]
    
#     def updatePos(self) -> None:
#         x,y = self.gate.pos
#         true_x = self.scene.grid.x(x)
#         true_y = self.scene.grid.y(x,y[1])
#         self.setPos(true_x,true_y)
    
#     def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mousePressEvent(e)
#         self.setZValue(2)

#     def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mouseMoveEvent(e)
#         for edge in self.edges: edge.updatePos()
    
#     def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
#         super().mouseReleaseEvent(e)
#         self.setZValue(1)
#         for item in self.scene.placeholders:
#             if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
#                 y_item = item.pos[1]
#                 if type(y_item)==int:y_item=[y_item]
#                 self.gate.pos = (item.pos[0],[y_item[0]+i for i in range(self.gate.dom)])

#                 # x,y = item.pos
#                 # if type(y) == int: y = [y]
#                 # true_x = self.scene.grid.x(x)
#                 # true_y = self.scene.grid.y(x,y[0])
#                 # self.setPos(true_x,true_y)
#                 self.updatePos()

#                 for edge in self.edges: edge.updatePos()
#                 return
#         # x,y = self.gate.pos
#         # if type(y) == int: y = [y]
#         # true_x = self.scene.grid.x(x)
#         # true_y = self.scene.grid.y(x,y[0])
#         # self.setPos(true_x,true_y)
#         self.updatePos()
#         for edge in self.edges: edge.updatePos()

# # class GateItem(QGraphicsItemGroup):
# #     box_size = 30
# #     box_pen: QPen = QPen(QColor("black"), 2)
# #     font_size = 12
# #     font = QFont("Times", font_size)

# #     def __init__(self, scene: Scene, gate: Gate) -> None:
# #         super().__init__()
# #         self.scene = scene
# #         self.setZValue(1)

# #         self.edges = []
        
# #         self.gate = gate
# #         x,y = self.gate.pos
# #         if type(y) == int: y = [y]
# #         true_x = self.scene.grid.x(x)
# #         true_y_top = self.scene.grid.y(x,y[0])
# #         true_y_bottom = self.scene.grid.y(x,y[-1])

# #         self.box = QGraphicsRectItem()
# #         self.text = QGraphicsTextItem()
# #         self.text.setPlainText(self.gate.type)
# #         self.text.setDefaultTextColor(QColor("black"))
# #         self.text.setFont(self.font)
# #         self.text.setPos(-self.font_size+2,-self.font_size+2+(true_y_bottom-true_y_top)/2)
# #         self.box.setPen(self.box_pen)
# #         self.box.setBrush(QColor("white"))
# #         self.box.setRect(-self.box_size/2,-self.box_size/2,self.box_size,true_y_bottom-true_y_top+self.box_size)
# #         self.addToGroup(self.box)
# #         self.addToGroup(self.text)
# #         self.setPos(true_x,true_y_top)


# #         self.input_pos = []
# #         self.output_pos = []

# #         for i in range(self.gate.dom):
# #             self.input_pos.append((-self.box_size/2,0))
# #             self.output_pos.append((self.box_size/2,0))

# #         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
# #         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
    
# #     def updatePos(self) -> None:
# #         # utiliser cette methode dans le init pour pas dupliquer le code
# #         x,y = self.gate.pos
# #         if type(y) == int: y = [y]
# #         true_x = self.scene.grid.x(x)
# #         true_y_top = self.scene.grid.y(x,y[0])
# #         self.setPos(true_x,true_y_top)

# #     def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
# #         super().mousePressEvent(e)
# #         self.setZValue(2)

# #     def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
# #         super().mouseMoveEvent(e)
# #         for edge in self.edges: edge.updatePos()
    
# #     def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
# #         super().mouseReleaseEvent(e)
# #         self.setZValue(1)
# #         for item in self.scene.placeholders:
# #             if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):

# #                 y_item = item.pos[1]
# #                 if type(y_item)==int:y_item=[y_item]
# #                 self.gate.pos = (item.pos[0],[y_item[0]+i for i in range(self.gate.dom)])
# #                 # self.gate.pos = item.pos # problème quand la porte à plusieurs entrée

# #                 x,y = item.pos
# #                 if type(y) == int: y = [y]
# #                 true_x = self.scene.grid.x(x)
# #                 true_y = self.scene.grid.y(x,y[0])
# #                 self.setPos(true_x,true_y)
# #                 for edge in self.edges: edge.updatePos()
# #                 return
# #         x,y = self.gate.pos
# #         if type(y) == int: y = [y]
# #         true_x = self.scene.grid.x(x)
# #         true_y = self.scene.grid.y(x,y[0])
# #         self.setPos(true_x,true_y)
# #         for edge in self.edges: edge.updatePos()





# # class CnotItem(QGraphicsItemGroup):
# #     pen = QPen(QColor("black"), 2)
# #     color = QColor("black")
# #     control_radius = 4
# #     target_radius = 10

# #     def __init__(self, scene: Scene, gate: Gate) -> None:
# #         super().__init__()
# #         self.scene = scene
# #         self.gate = gate
# #         x,y = self.gate.pos

# #         self.edges = []

# #         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
# #         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        
        

# #         true_y_control = self.scene.grid.y(x,y[0])
# #         true_y_target = self.scene.grid.y(x,y[1])

# #         true_x = self.scene.grid.x(x)
# #         true_y = true_y_control

# #         self.controlItem = QGraphicsEllipseItem()
# #         self.controlItem.setPen(self.pen)
# #         self.controlItem.setBrush(self.color)
# #         self.controlItem.setRect(-self.control_radius,-self.control_radius,2*self.control_radius,2*self.control_radius)
# #         self.addToGroup(self.controlItem)

# #         # self.controlItem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
# #         # def mousePressEventControl(self) -> None:
# #         #     print("OURA")
# #         # self.controlItem.mousePressEvent = mousePressEventControl
# #         # self.controlItem.setCursor(Qt.SizeVerCursor)

        

# #         self.targetItem = QGraphicsPathItem()
# #         self.targetItem.setPen(self.pen)
# #         path = QPainterPath()
# #         target_padding = GateItem.box_size/2-self.target_radius
# #         target_size = 2*self.target_radius
# #         target_relative_y = true_y_target-true_y_control
# #         path.addEllipse(-self.target_radius,target_relative_y-self.target_radius,target_size,target_size)
# #         path.moveTo(0,0)
# #         path.lineTo(0,target_relative_y+self.target_radius) # vertical line
# #         path.moveTo(-self.target_radius,target_relative_y)
# #         path.lineTo(self.target_radius,target_relative_y)
# #         self.targetItem.setPath(path)
# #         self.addToGroup(self.targetItem)

# #         self.targetItem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        
# #         self.setPos(true_x,true_y)

# #         self.input_pos = [
# #             (0,0),
# #             (-self.target_radius,0)
# #         ]
# #         self.output_pos = [
# #             (0,0),
# #             (self.target_radius,0)
# #         ]

# #     def updatePos(self) -> None:
# #         pass
        

class DividerItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()


class GathererItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()