from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup, QGraphicsPolygonItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem
from engine.circuit import Gate
from .scene import Scene

class GateItem(QGraphicsRectItem):
    def __init__(self, scene: Scene, Grgate: Gate) -> None:
        super().__init__()


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
    def __init__(self) -> None:
        super().__init__()