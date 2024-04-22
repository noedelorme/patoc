from PySide6.QtCore import Qt, QPointF, QSizeF
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsItemGroup
from PySide6.QtGui import QBrush, QColor, QPen, QRadialGradient, QGradient, QPainterPath

from engine.circuit import Circuit, Gate
from engine.grid import Grid
from .gate_items import GateGroup, BoundItem, ControlledGateGroup
from .edge_items import EdgeItem

from data.examples import czLHS, circuit1, subcircuit1, circuit2, connectivity
from .utils import *

class Scene(QGraphicsScene):
    """Class for managing the graphical items"""

    grid_size = 200
    grid_offset = 20
    real_grid_radius = grid_size*grid_offset
    grid_pen = QPen(QColor(0, 0, 0, 15), 1)
    grid_pen_bold = QPen(QColor(0, 0, 0, 15), 2)
    
    def __init__(self) -> None:
        super().__init__()

        self.circuit = None

        self.setCircuit(circuit2)
        self.setBackgroundBrush(QColor("white"))
        real_grid_size = self.grid_size*self.grid_offset
        self.setSceneRect(-self.real_grid_radius,-self.real_grid_radius,2*self.real_grid_radius,2*self.real_grid_radius)

        self.drawGrid()
        self.computeDefaultCoords()
        self.drawCircuit()
        


        gate = Gate("[3]X", id=None, dom=5, cod=4, pos=(0,[-16,-15,-13,-11,-8],[-16,-15,-13,-11]))
        mtn = GateGroup(self, gate)


    def setCircuit(self, circuit: Circuit) -> None:
        self.circuit = circuit

    def getPoint(self, x, y) -> QPointF:
        return QPointF(x*self.grid_offset, y*self.grid_offset)
    
    def drawGrid(self) -> None:
        for i in range(-self.grid_size,self.grid_size+1):
            line = QGraphicsLineItem()
            line.setZValue(0)
            if i%2 == 0: line.setPen(self.grid_pen_bold)
            else: line.setPen(self.grid_pen)
            line.setLine(0,0,2*self.real_grid_radius,0)
            line.setPos(-self.real_grid_radius,i*self.grid_offset)
            self.addItem(line)
        for i in range(-self.grid_size,self.grid_size+1):
            line = QGraphicsLineItem()
            line.setZValue(0)
            if i%2 == 0: line.setPen(self.grid_pen_bold)
            else: line.setPen(self.grid_pen)
            line.setLine(0,0,0,2*self.real_grid_radius)
            line.setPos(i*self.grid_offset,-self.real_grid_radius)
            self.addItem(line)
    
    def computeDefaultCoords(self) -> None:
        self.circuit.updateDepth()
        self.nb_cols = self.circuit.depth+1
        current_ys = [-5 for i in range(self.nb_cols)]

        for gate in self.circuit.gates:
            depth = gate.depth if gate.type != "out" else self.circuit.depth
            x = 4*depth - 15
            input_ys = [current_ys[depth]+2*i for i in range(gate.dom)]
            output_ys = [current_ys[depth]+2*i for i in range(gate.cod)]
            current_ys[depth] = max(input_ys+output_ys)+3
            gate.pos = (x, input_ys, output_ys)
    
    def drawCircuit(self) -> None:
        for gate in self.circuit.gates:
            if gate.type == "in" or gate.type=="out":
                gate.gate_item = BoundItem(self, gate)
            else:
                gate.gate_item = GateGroup(self, gate)

        queue = self.circuit.org.copy()
        visited = [(i in queue) for i in range(len(self.circuit.gates))]
        while len(queue)>0:
            current_id = queue.pop(0)
            current_gate = self.circuit.gates[current_id]
            for (id_pred,wiring) in current_gate.preset:
                pred_gate = self.circuit.gates[id_pred]
                edge = EdgeItem(self, pred_gate.gate_item, current_gate.gate_item, wiring)
                self.addItem(edge)
            for (id_succ,wiring) in current_gate.postset:
                if not visited[id_succ]:
                    queue.append(id_succ)
                    visited[id_succ] = True


class SceneView(QGraphicsView):
    """Class for displaying the contents of a QGraphicsScene"""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        super().__init__(self.scene)