from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QColor, QPen

from .gate_items import GateItem, NotItem, ControlItem

if TYPE_CHECKING:
    from .scene import Scene

class EdgeItem(QGraphicsLineItem):
    pen: QPen = QPen(QColor("black"), 2)

    def __init__(self, scene: Scene, s, t, wiring) -> None:
        super().__init__()
        self.scene = scene

        self.s = s
        self.t = t
        self.wiring = wiring

        self.s.edges.append(self)
        self.t.edges.append(self)

        # x0,y0,x1,y1 = None,None,None,None
        # if self.s.gate.type == "CNOT": x0,y0 = self.s.output_pos[0]
        # else: x0,y0 = self.s.output_pos[wiring[0]]
        # if self.t.gate.type == "CNOT": x1,y1 = self.t.input_pos[0]
        # else: x1,y1 = self.t.input_pos[wiring[1]]

        # x_s,y_s = s.gate.pos
        # if type(y_s) == int: y_s = [y_s]
        # true_x_s = self.scene.grid.x(x_s)
        # true_y_s = self.scene.grid.y(x_s,y_s[wiring[0]])
        # x_t,y_t = t.gate.pos
        # if type(y_t) == int: y_t = [y_t]
        # true_x_t = self.scene.grid.x(x_t)
        # true_y_t = self.scene.grid.y(x_t,y_t[wiring[1]])

        # self.setPos(true_x_s+x0,true_y_s+y0)
        # dest_x = (true_x_t+x1)-(true_x_s+x0)
        # dest_y = (true_y_t+y1)-(true_y_s+y0)
        # self.setLine(0,0,dest_x,dest_y)
        # self.setPen(self.pen)
        self.updatePos()
    
    def updatePos(self) -> None:
        # x0,y0,x1,y1 = None,None,None,None
        # if self.s.gate.type == "CNOT": x0,y0 = self.s.output_pos[0]
        # else: x0,y0 = self.s.output_pos[self.wiring[0]]
        # if self.t.gate.type == "CNOT": x1,y1 = self.t.input_pos[0]
        # else: x1,y1 = self.t.input_pos[self.wiring[1]]

        x0,y0 = self.s.output_pos[self.wiring[0]]
        x1,y1 = self.t.input_pos[self.wiring[1]]

        x_s,y_s = self.s.gate.pos
        if type(y_s) == int: y_s = [y_s]
        x_t,y_t = self.t.gate.pos
        if type(y_t) == int: y_t = [y_t]

        if isinstance(self.s, ControlItem): y_s = [y_s[0]]
        if isinstance(self.s, NotItem): y_s = [y_s[1]]
        if isinstance(self.t, ControlItem): y_t = [y_t[0]]
        if isinstance(self.t, NotItem): y_t = [y_t[1]]

        # print("wiring", self.wiring)


        true_x_s = self.s.pos().x()
        true_y_s = self.s.pos().y()+self.scene.grid.y(x_s,y_s[self.wiring[0]])-self.scene.grid.y(x_s,y_s[0])
        # if self.s.gate.type == "CNOT": true_y_s = self.s.pos().y()
        true_x_t = self.t.pos().x()
        true_y_t = self.t.pos().y()+self.scene.grid.y(x_t,y_t[self.wiring[1]])-self.scene.grid.y(x_t,y_t[0])
        # if self.t.gate.type == "CNOT": true_y_t = self.t.pos().y()
        
        self.setPos(true_x_s+x0,true_y_s+y0)
        dest_x = (true_x_t+x1)-(true_x_s+x0)
        dest_y = (true_y_t+y1)-(true_y_s+y0)
        self.setLine(0,0,dest_x,dest_y)
        self.setPen(self.pen)