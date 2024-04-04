from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QBrush, QColor, QPen, QRadialGradient, QGradient

from engine.circuit import Circuit, Gate
from .items import GateItem, PlaceholderItem, EdgeItem, BoundItem, CnotItem
from .grid import Grid

from data.examples import czLHS, circuit1, subcircuit1

class Scene(QGraphicsScene):
    """Class for managing the graphical items"""
    
    def __init__(self) -> None:
        super().__init__()

        self.circuit = circuit1
        self.setBackgroundBrush(QColor("white"))

        self.grid = Grid()
        self.grid.setCircuit(circuit1)
        print(self.grid.nb_cols)
        print(self.grid.nb_rows)
        print(self.grid.grid)
        print(self.grid.true_x)
        print(self.grid.true_y)

        self.drawPlaceholders()
        self.drawCircuit()

    def setCircuit(self, circuit: Circuit) -> None:
        self.circuit = circuit

    def drawPlaceholders(self) -> None:
        for i in range(self.grid.nb_cols):
            for j in range(self.grid.nb_rows[i]):
                place = PlaceholderItem(self, (i,j))
                self.addItem(place)

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
        edge = EdgeItem(s,t, wiring)
        self.addItem(edge)
    
    def drawCircuit(self):
        for gate in self.circuit.gates: self.drawGate(gate)

        # queue = self.circuit.org.copy()
        # visited = [(i in queue) for i in range(len(self.circuit.gates))]
        # while len(queue)>0:
        #     current_id = queue.pop(0)
        #     current_gate = self.circuit.gates[current_id]
        #     x,y = current_gate.pos
        #     if type(y) == int: y = [y]
        #     for (id_pred,wiring) in current_gate.preset:
        #         pred_gate = self.circuit.gates[id_pred]
        #         x_pred,y_pred = pred_gate.pos
        #         if type(y_pred) == int: y_pred = [y_pred]

        #         self.drawEdge(pred_gate.gate_item, current_gate.gate_item, wiring)

        #         # if gatepred.type == "D" or gatepred.type == "G":
        #         #     self.canvas.create_line(self.x(xpred),self.y(x,y[wiring[1]]),self.x(x),self.y(x,y[wiring[1]]), fill="black", width=1)
        #         # else:
        #         #     if currentgate.type == "G":
        #         #         self.canvas.create_line(self.x(xpred),self.y(xpred,ypred[wiring[0]]),self.x(x),self.y(xpred,ypred[wiring[0]]), fill="black", width=1)
        #         #         pass
        #         #     else:
        #         #         self.canvas.create_line(self.x(xpred),self.y(xpred,ypred[wiring[0]]),self.x(x),self.y(x,y[wiring[1]]), fill="black", width=1)
        #     for (id_succ,wiring) in current_gate.postset:
        #         if not visited[id_succ]:
        #             queue.append(id_succ)
        #             visited[id_succ] = True
            



            # if gate.type == "D":
            #     succ0 = self.circuit.gates[gate.postset[0][0]]
            #     wiring0 = gate.postset[0][1]
            #     succ1 = self.circuit.gates[gate.postset[1][0]]
            #     wiring1 = gate.postset[1][1]
            #     xsucc0,ysucc0 = succ0.pos
            #     if type(ysucc0) == int: ysucc0 = [ysucc0]
            #     xsucc1,ysucc1 = succ1.pos
            #     if type(ysucc1) == int: ysucc1 = [ysucc1]
            #     self.canvas.create_line(self.x(x),self.y(xsucc0,ysucc0[wiring0[1]]),self.x(x),self.y(xsucc1,ysucc1[wiring1[1]]), fill="black", width=1)
            # elif gate.type == "G":
            #     self.canvas.create_line(self.x(x),self.y(x,y),self.x(x),self.y(x,y+1), fill="black", width=1)
                

    



class SceneView(QGraphicsView):
    """Class for displaying the contents of a QGraphicsScene"""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        super().__init__(self.scene)