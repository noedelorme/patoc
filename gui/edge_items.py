from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsPathItem
from PySide6.QtGui import QColor, QPen, QPainterPath

from .gate_items import GateItemGroup

from .utils import *

if TYPE_CHECKING:
    from .scene import Scene


class EdgeItem(QGraphicsPathItem):
    pen: QPen = QPen(QColor("black"), 2.5)

    def __init__(self, scene: Scene, s, t, wiring) -> None:
        super().__init__()
        self.scene = scene
        self.setZValue(1)
        self.setPen(self.pen)

        self.s = s
        self.t = t
        self.wiring = wiring

        self.s.edges.append(self)
        self.t.edges.append(self)

        self.path = QPainterPath()
        self.update()
    
    def update(self) -> None:
        x1 = self.s.outputs[self.wiring[0]].pos().x()
        y1 = self.s.outputs[self.wiring[0]].pos().y()
        x2 = self.t.inputs[self.wiring[1]].pos().x()
        y2 = self.t.inputs[self.wiring[1]].pos().y()
        delta_x = x2-x1
        delta_y = y2-y1
        self.setPos(x1, y1)
        self.path.clear()
        self.path.cubicTo(delta_x/2, 0, delta_x/2, delta_y, delta_x, delta_y)
        self.setPath(self.path)