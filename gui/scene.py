from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PySide6.QtGui import QBrush, QColor, QPen, QRadialGradient, QGradient

from engine.circuit import Circuit, Gate
from .items import GateItem, PlaceholderItem, EdgeItem, BoundItem
from .grid import Grid

from data.examples import czLHS, circuit1, subcircuit1

class Scene(QGraphicsScene):
    """Class for managing the graphical items"""
    
    def __init__(self) -> None:
        super().__init__()

        self.circuit = czLHS

        self.setBackgroundBrush(QColor("white"))
        

        # gate_item1 = GateItem(self, Gate(0, "A", pos=(0,0)))
        # gate_item2 = GateItem(self, Gate(0, "B", pos=(3,0)))
        # gate_item3 = GateItem(self, Gate(0, "C", pos=(4,1)))
        # self.addItem(gate_item1)
        # self.addItem(gate_item2)
        # self.addItem(gate_item3)

        # edge1 = EdgeItem(None,None)
        # self.addItem(edge1)

        self.grid = Grid()
        self.grid.setCircuit(czLHS)
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

        # for i in range(10):
        #     for j in range(6):
        #         place = PlaceholderItem((i,j))
        #         self.addItem(place)
    
    def drawCircuit(self):
        # # draw wires
        # queue = self.circuit.org.copy()
        # visited = [False for i in range(len(self.circuit.gates))]
        # while len(queue)>0:
        #     currentid = queue.pop(0)
        #     currentgate = self.circuit.gates[currentid]
        #     x,y = currentgate.pos
        #     if type(y) == int: y = [y]
        #     for (idpred,wiring) in currentgate.preset:
        #         gatepred = self.circuit.gates[idpred]
        #         xpred,ypred = gatepred.pos
        #         if type(ypred) == int: ypred = [ypred]
        #         if gatepred.type == "D" or gatepred.type == "G":
        #             self.canvas.create_line(self.x(xpred),self.y(x,y[wiring[1]]),self.x(x),self.y(x,y[wiring[1]]), fill="black", width=1)
        #         else:
        #             if currentgate.type == "G":
        #                 self.canvas.create_line(self.x(xpred),self.y(xpred,ypred[wiring[0]]),self.x(x),self.y(xpred,ypred[wiring[0]]), fill="black", width=1)
        #                 pass
        #             else:
        #                 self.canvas.create_line(self.x(xpred),self.y(xpred,ypred[wiring[0]]),self.x(x),self.y(x,y[wiring[1]]), fill="black", width=1)
        #     for (idsucc,wiring) in currentgate.postset:
        #         if not visited[idsucc]:
        #             queue.append(idsucc)
        #             visited[idsucc] = True

        # draw gates
        for gate in self.circuit.gates:
            if gate.type == "in" or gate.type == "out":
                bound_item = BoundItem(self, gate)
                self.addItem(bound_item)
            else:
                gate_item = GateItem(self, gate)
                self.addItem(gate_item)
            # elif gate.type == "CNOT":
            #     self.cnot(gate)
            # elif gate.type == "D":
            #     self.divider(x,y)
            # elif gate.type == "G":
            #     self.gatherer(x,y)
            # else:
            #     self.gate(gate)
            
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