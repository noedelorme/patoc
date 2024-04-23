from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsPathItem
from PySide6.QtGui import QColor, QPen, QPainterPath

from .gate_items import GateGroup, BoundItem

from .utils import *

if TYPE_CHECKING:
    from .scene import Scene


class EdgeItem(QGraphicsPathItem):
    pen: QPen = QPen(QColor("black"), 2)

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
        nb_controls_s = 0 if isinstance(self.s, BoundItem) else self.s.nb_controls
        nb_controls_t = 0 if isinstance(self.t, BoundItem) else self.t.nb_controls
        outputs_s = self.s.controls if self.wiring[0]<nb_controls_s else self.s.outputs
        inputs_t = self.t.controls if self.wiring[1]<nb_controls_t else self.t.inputs
        x1 = outputs_s[self.wiring[0]-nb_controls_s].pos().x()
        y1 = outputs_s[self.wiring[0]-nb_controls_s].pos().y()
        x2 = inputs_t[self.wiring[1]-nb_controls_t].pos().x()
        y2 = inputs_t[self.wiring[1]-nb_controls_t].pos().y()
        delta_x = x2-x1
        delta_y = y2-y1
        self.setPos(x1, y1)
        self.path.clear()
        self.path.cubicTo(delta_x/2, 0, delta_x/2, delta_y, delta_x, delta_y)
        self.setPath(self.path)