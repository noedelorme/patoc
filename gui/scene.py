from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsLineItem
from PySide6.QtGui import QBrush, QColor, QPen, QRadialGradient, QGradient

from engine.circuit import Circuit, Gate
from .items import GateItem, PlaceholderItem, EdgeItem, BoundItem, CnotItem, GridLineItem
from .grid import Grid

from data.examples import czLHS, circuit1, subcircuit1

class Scene(QGraphicsScene):
    """Class for managing the graphical items"""

    
    def __init__(self) -> None:
        super().__init__()

        self.circuit = circuit1
        self.setBackgroundBrush(QColor("white"))
        self.setSceneRect(-100,-100,900,500)

        self.grid = Grid()
        self.grid.setCircuit(circuit1)

        self.drawPlaceholders()
        self.drawLayers()
        self.drawCircuit()

    def setCircuit(self, circuit: Circuit) -> None:
        self.circuit = circuit

    def drawPlaceholders(self) -> None:
        for i in range(self.grid.nb_cols):
            for j in range(self.grid.nb_rows[i]):
                if self.grid.grid[i][j] == None:
                    place = PlaceholderItem(self, (i,j))
                    self.addItem(place)
    
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
            cnot_item = CnotItem(self, gate)
            gate.gate_item = cnot_item
            self.addItem(cnot_item)
        else:
            gate_item = GateItem(self, gate)
            gate.gate_item = gate_item
            self.addItem(gate_item)
    
    def drawEdge(self, s, t, wiring) -> None:
        edge = EdgeItem(self, s,t, wiring)
        s.edges.append(edge)
        t.edges.append(edge)
        self.addItem(edge)
    
    def drawCircuit(self) -> None:
        for gate in self.circuit.gates:
            if gate.isSparseGate():
                print("Sparse gates are not yet implemented.")
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
                self.drawEdge(pred_gate.gate_item, current_gate.gate_item, wiring)
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