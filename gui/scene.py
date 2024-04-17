from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsLineItem
from PySide6.QtGui import QBrush, QColor, QPen, QRadialGradient, QGradient, QPainterPath

from engine.circuit import Circuit, Gate
from engine.grid import Grid
from .vanity_items import PlaceholderItem, BoundItem, GridLineItem
from .gate_items import GateItem, NotItem, ControlItem
from .edge_items import EdgeItem

from data.examples import czLHS, circuit1, subcircuit1, circuit2

class Scene(QGraphicsScene):
    """Class for managing the graphical items"""
    
    def __init__(self) -> None:
        super().__init__()

        self.circuit = circuit1
        self.setBackgroundBrush(QColor("white"))
        self.setSceneRect(-100,-100,900,500)

        self.grid = Grid(circuit1)

        self.placeholders = []

        self.drawPlaceholders()
        self.drawLayers()
        self.drawCircuit()

        # # pur faire des arcs
        # path = QPainterPath()
        # path.addRect(20, 20, 60, 60)
        # path.moveTo(0, 0)
        # path.cubicTo(99, 0, 50, 50, 99, 99)
        # path.cubicTo(0, 99, 50, 50, 0, 0)
        # mtn = QGraphicsPathItem()
        # mtn.setPath(path)
        # pen = QPen(QColor("black"), 2)
        # mtn.setPen(pen)
        # self.addItem(mtn)

    def setCircuit(self, circuit: Circuit) -> None:
        self.circuit = circuit

    def drawPlaceholders(self) -> None:
        for i in range(self.grid.nb_cols):
            for j in range(self.grid.nb_rows[i]):
                if self.grid.grid[i][j] == None:
                    place = PlaceholderItem(self, (i,j))
                    self.placeholders.append(place)
                    self.addItem(place)
                    self.grid.grid[i][j] = place
    
    def drawLayers(self) -> None:
        for i in range(self.grid.nb_cols):
            line = GridLineItem(self, i)
            self.addItem(line)

    def drawGate(self, gate: Gate) -> None:
        if gate.type == "in" or gate.type == "out":
            bound_item = BoundItem(self, gate)
            gate.gate_item = bound_item
            self.addItem(bound_item)
        elif gate.type == "CNOT":
            # cnot_item = CnotItem(self, gate)
            # gate.gate_item = cnot_item
            # self.addItem(cnot_item)

            control = ControlItem(self, gate)
            target = NotItem(self, gate)
            gate.gate_item = [control,target]
            self.addItem(control)
            self.addItem(target)
        else:
            gate_item = GateItem(self, gate)
            gate.gate_item = gate_item
            self.addItem(gate_item)
    
    def drawEdge(self, s, t, wiring) -> None:
        s_item = s.gate_item
        t_item = t.gate_item
        if s.type == "CNOT":
            s_item = s.gate_item[wiring[0]]
            # wiring[0] = 0
            wiring = (0,wiring[1])
        if t.type == "CNOT":
            t_item = t.gate_item[wiring[1]]
            # wiring[1] = 0
            wiring = (wiring[0],0)
        edge = EdgeItem(self, s_item, t_item, wiring)
        self.addItem(edge)
    
    def drawCircuit(self) -> None:
        for gate in self.circuit.gates:
            self.drawGate(gate)

        queue = self.circuit.org.copy()
        visited = [(i in queue) for i in range(len(self.circuit.gates))]
        while len(queue)>0:
            current_id = queue.pop(0)
            current_gate = self.circuit.gates[current_id]
            x,y = current_gate.pos
            if type(y) == int: y = [y]
            for (id_pred,wiring) in current_gate.preset:
                pred_gate = self.circuit.gates[id_pred]
                x_pred,y_pred = pred_gate.pos
                if type(y_pred) == int: y_pred = [y_pred]
                self.drawEdge(pred_gate, current_gate, wiring)
            for (id_succ,wiring) in current_gate.postset:
                if not visited[id_succ]:
                    queue.append(id_succ)
                    visited[id_succ] = True
    
    def updatePos(self) -> None:
        for item in self.items():
            if isinstance(item, GridLineItem) or isinstance(item, GateItem) or isinstance(item, BoundItem) or isinstance(item, EdgeItem) or isinstance(item, PlaceholderItem):
                item.updatePos()



class SceneView(QGraphicsView):
    """Class for displaying the contents of a QGraphicsScene"""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        super().__init__(self.scene)