from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QPointF, QSizeF, QRectF
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QColor, QFont, QPen, QBrush, QPainterPath, QCursor
from engine.circuit import Gate

if TYPE_CHECKING:
    from .scene import Scene


class GateItemGroup:
    box_size = 30
    box_pen: QPen = QPen(QColor("black"), 2)
    font_size = 12
    font = QFont("Times", font_size)
    port_size = 5
    port_pen = QPen(QColor("blue"), 1)
    port_brush = QBrush(QColor("blue"))

    def __init__(self, scene: Scene, gate: Gate) -> None:
        self.scene = scene
        self.gate = gate
        x,yin,yout = self.gate.pos
        min_y,max_y = min(yin+yout),max(yin+yout)
        true_x = x*self.scene.grid_offset
        true_min_y = min_y*self.scene.grid_offset
        true_max_y = max_y*self.scene.grid_offset
        height = true_max_y-true_min_y+self.scene.grid_offset

        self.box = QGraphicsRectItem()
        self.box.setPen(self.box_pen)
        self.box.setBrush(QColor("white"))
        self.box.setRect(-self.box_size/2,-self.scene.grid_offset/2,self.box_size,height)
        self.box.setPos(true_x,true_min_y)
        self.scene.addItem(self.box)


        def mouseMoveEventPort(e: QGraphicsSceneMouseEvent) -> None:
            self.setPos(e.scenePos().x(),0)

        self.inputs = []
        for i in range(self.gate.dom):
            port = QGraphicsRectItem()
            y = yin[i]
            true_y = y*self.scene.grid_offset
            port.setPen(self.port_pen)
            port.setBrush(self.port_brush)
            port.setRect(-self.port_size/2,-self.port_size/2,self.port_size,self.port_size)
            self.inputs.append(port)
            port.setPos(true_x-self.box_size/2,true_y)
            self.scene.addItem(port)

            port.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            port.mouseMoveEvent = mouseMoveEventPort
        
        self.outputs = []
        for i in range(self.gate.cod):
            port = QGraphicsRectItem()
            y = yout[i]
            true_y = y*self.scene.grid_offset
            port.setPen(self.port_pen)
            port.setBrush(self.port_brush)
            port.setRect(-self.port_size/2,-self.port_size/2,self.port_size,self.port_size)
            self.outputs.append(port)
            port.setPos(true_x+self.box_size/2,true_y)
            self.scene.addItem(port)

            port.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            port.mouseMoveEvent = mouseMoveEventPort



        self.text = QGraphicsTextItem()
        self.text.setPlainText(self.gate.type)
        self.text.setDefaultTextColor(QColor("black"))
        self.text.setFont(self.font)
        self.text.setPos(true_x-self.font_size+2,-self.font_size+2+(true_min_y+true_max_y)/2)
        self.scene.addItem(self.text)








# class DraggableItem(QGraphicsItemGroup):
#     def __init__(self, scene: Scene, gate: Gate) -> None:
#         super().__init__()

#         self.scene = scene
#         self.gate = gate
#         self.setZValue(1)

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

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

class GateItem(QGraphicsItemGroup):
    box_size = 30
    box_pen: QPen = QPen(QColor("black"), 2)
    font_size = 12
    font = QFont("Times", font_size)

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()

        self.scene = scene
        self.gate = gate
        self.setZValue(1)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.edges = []
        
        x,y = self.gate.pos
        if type(y) == int: y = [y]
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

        self.updatePos()

        self.input_pos = []
        self.output_pos = []

        for i in range(self.gate.dom):
            self.input_pos.append((-self.box_size/2,0))
            self.output_pos.append((self.box_size/2,0))
    
    def updatePos(self) -> None:
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
        for item in self.scene.placeholders:
            if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
                y_item = item.pos[1]
                if type(y_item)==int:y_item=[y_item]
                self.gate.pos = (item.pos[0],[y_item[0]+i for i in range(self.gate.dom)])

                self.updatePos()

                for edge in self.edges: edge.updatePos()
                return
        self.updatePos()
        for edge in self.edges: edge.updatePos()

class ControlItem(QGraphicsItemGroup):
    pen = QPen(QColor("black"), 2)
    color = QColor("black")
    radius = 4

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()

        self.scene = scene
        self.gate = gate
        self.setZValue(1)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.edges = []
    
        self.bullet = QGraphicsEllipseItem()
        self.bullet.setPen(self.pen)
        self.bullet.setBrush(self.color)
        self.bullet.setRect(-self.radius,-self.radius,2*self.radius,2*self.radius)
        self.addToGroup(self.bullet)

        self.updatePos()

        self.input_pos = [(-self.radius,0)]
        self.output_pos = [(self.radius,0)]
    
    def updatePos(self) -> None:
        x,y = self.gate.pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y[0])
        self.setPos(true_x,true_y)
    
    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)
        self.setZValue(2)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(e)
        for edge in self.edges: edge.updatePos()
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        self.setZValue(1)
        for item in self.scene.placeholders:
            if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
                y_item = item.pos[1]
                if type(y_item)==int:y_item=[y_item]
                self.gate.pos = (item.pos[0],[y_item[0]+i for i in range(self.gate.dom)])

                # x,y = item.pos
                # if type(y) == int: y = [y]
                # true_x = self.scene.grid.x(x)
                # true_y = self.scene.grid.y(x,y[0])
                # self.setPos(true_x,true_y)
                self.updatePos()

                for edge in self.edges: edge.updatePos()
                return
        # x,y = self.gate.pos
        # if type(y) == int: y = [y]
        # true_x = self.scene.grid.x(x)
        # true_y = self.scene.grid.y(x,y[0])
        # self.setPos(true_x,true_y)
        self.updatePos()
        for edge in self.edges: edge.updatePos()


class NotItem(QGraphicsItemGroup):
    pen = QPen(QColor("black"), 2)
    color = QColor("black")
    radius = 10

    def __init__(self, scene: Scene, gate: Gate) -> None:
        super().__init__()

        self.scene = scene
        self.gate = gate
        self.setZValue(1)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.edges = []
    
        self.oplus = QGraphicsPathItem()
        self.oplus.setPen(self.pen)
        path = QPainterPath()
        path.addEllipse(-self.radius,-self.radius,2*self.radius,2*self.radius)
        path.moveTo(-self.radius,0)
        path.lineTo(self.radius,0)
        path.moveTo(0,-self.radius)
        path.lineTo(0,self.radius)
        self.oplus.setPath(path)
        self.addToGroup(self.oplus)

        self.updatePos()

        self.input_pos = [(-self.radius,0)]
        self.output_pos = [(self.radius,0)]
    
    def updatePos(self) -> None:
        x,y = self.gate.pos
        true_x = self.scene.grid.x(x)
        true_y = self.scene.grid.y(x,y[1])
        self.setPos(true_x,true_y)
    
    def mousePressEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(e)
        self.setZValue(2)

    def mouseMoveEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(e)
        for edge in self.edges: edge.updatePos()
    
    def mouseReleaseEvent(self, e: QGraphicsSceneMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        self.setZValue(1)
        for item in self.scene.placeholders:
            if item.sceneBoundingRect().intersects(self.sceneBoundingRect()):
                y_item = item.pos[1]
                if type(y_item)==int:y_item=[y_item]
                self.gate.pos = (item.pos[0],[y_item[0]+i for i in range(self.gate.dom)])

                # x,y = item.pos
                # if type(y) == int: y = [y]
                # true_x = self.scene.grid.x(x)
                # true_y = self.scene.grid.y(x,y[0])
                # self.setPos(true_x,true_y)
                self.updatePos()

                for edge in self.edges: edge.updatePos()
                return
        # x,y = self.gate.pos
        # if type(y) == int: y = [y]
        # true_x = self.scene.grid.x(x)
        # true_y = self.scene.grid.y(x,y[0])
        # self.setPos(true_x,true_y)
        self.updatePos()
        for edge in self.edges: edge.updatePos()

# class GateItem(QGraphicsItemGroup):
#     box_size = 30
#     box_pen: QPen = QPen(QColor("black"), 2)
#     font_size = 12
#     font = QFont("Times", font_size)

#     def __init__(self, scene: Scene, gate: Gate) -> None:
#         super().__init__()
#         self.scene = scene
#         self.setZValue(1)

#         self.edges = []
        
#         self.gate = gate
#         x,y = self.gate.pos
#         if type(y) == int: y = [y]
#         true_x = self.scene.grid.x(x)
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
#         self.setPos(true_x,true_y_top)


#         self.input_pos = []
#         self.output_pos = []

#         for i in range(self.gate.dom):
#             self.input_pos.append((-self.box_size/2,0))
#             self.output_pos.append((self.box_size/2,0))

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
    
#     def updatePos(self) -> None:
#         # utiliser cette methode dans le init pour pas dupliquer le code
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
#                 # self.gate.pos = item.pos # problème quand la porte à plusieurs entrée

#                 x,y = item.pos
#                 if type(y) == int: y = [y]
#                 true_x = self.scene.grid.x(x)
#                 true_y = self.scene.grid.y(x,y[0])
#                 self.setPos(true_x,true_y)
#                 for edge in self.edges: edge.updatePos()
#                 return
#         x,y = self.gate.pos
#         if type(y) == int: y = [y]
#         true_x = self.scene.grid.x(x)
#         true_y = self.scene.grid.y(x,y[0])
#         self.setPos(true_x,true_y)
#         for edge in self.edges: edge.updatePos()





# class CnotItem(QGraphicsItemGroup):
#     pen = QPen(QColor("black"), 2)
#     color = QColor("black")
#     control_radius = 4
#     target_radius = 10

#     def __init__(self, scene: Scene, gate: Gate) -> None:
#         super().__init__()
#         self.scene = scene
#         self.gate = gate
#         x,y = self.gate.pos

#         self.edges = []

#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
#         self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        
        

#         true_y_control = self.scene.grid.y(x,y[0])
#         true_y_target = self.scene.grid.y(x,y[1])

#         true_x = self.scene.grid.x(x)
#         true_y = true_y_control

#         self.controlItem = QGraphicsEllipseItem()
#         self.controlItem.setPen(self.pen)
#         self.controlItem.setBrush(self.color)
#         self.controlItem.setRect(-self.control_radius,-self.control_radius,2*self.control_radius,2*self.control_radius)
#         self.addToGroup(self.controlItem)

#         # self.controlItem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
#         # def mousePressEventControl(self) -> None:
#         #     print("OURA")
#         # self.controlItem.mousePressEvent = mousePressEventControl
#         # self.controlItem.setCursor(Qt.SizeVerCursor)

        

#         self.targetItem = QGraphicsPathItem()
#         self.targetItem.setPen(self.pen)
#         path = QPainterPath()
#         target_padding = GateItem.box_size/2-self.target_radius
#         target_size = 2*self.target_radius
#         target_relative_y = true_y_target-true_y_control
#         path.addEllipse(-self.target_radius,target_relative_y-self.target_radius,target_size,target_size)
#         path.moveTo(0,0)
#         path.lineTo(0,target_relative_y+self.target_radius) # vertical line
#         path.moveTo(-self.target_radius,target_relative_y)
#         path.lineTo(self.target_radius,target_relative_y)
#         self.targetItem.setPath(path)
#         self.addToGroup(self.targetItem)

#         self.targetItem.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        
#         self.setPos(true_x,true_y)

#         self.input_pos = [
#             (0,0),
#             (-self.target_radius,0)
#         ]
#         self.output_pos = [
#             (0,0),
#             (self.target_radius,0)
#         ]

#     def updatePos(self) -> None:
#         pass
        

class DividerItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()


class GathererItem(QGraphicsPolygonItem):
    def __init__(self) -> None:
        super().__init__()