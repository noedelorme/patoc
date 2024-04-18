from PySide6.QtCore import Qt, QPointF, QSizeF
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsItemGroup
from PySide6.QtGui import QBrush, QColor, QPen, QRadialGradient, QGradient, QPainterPath

from engine.circuit import Circuit, Gate
from engine.grid import Grid
from .vanity_items import PlaceholderItem, BoundItem, GridLineItem
from .gate_items import GateItem, NotItem, ControlItem, GateItemGroup
from .edge_items import EdgeItem

from data.examples import czLHS, circuit1, subcircuit1, circuit2

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

        self.setCircuit(circuit1)
        self.setBackgroundBrush(QColor("white"))
        real_grid_size = self.grid_size*self.grid_offset
        self.setSceneRect(-self.real_grid_radius,-self.real_grid_radius,2*self.real_grid_radius,2*self.real_grid_radius)

        self.drawGrid()
        self.computeDefaultCoords()

        gate = Gate("H", id=None, dom=3, cod=2, pos=(3,[0,2,6],[1,3]))
        mtn = GateItemGroup(self, gate)


        test = QGraphicsItemGroup()
        box = QGraphicsRectItem()
        box.setBrush(QColor("white"))
        box.setRect(0,0,30,30)
        box.setPos(-50,-30)
        box.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)

        
    
        self.addItem(box)


        # self.grid = Grid(circuit1)

        # self.placeholders = []

        # self.drawPlaceholders()
        # self.drawLayers()
        # self.drawCircuit()

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

    def getPoint(self, x, y) -> QPointF:
        return QPointF(x*self.grid_offset, y*self.grid_offset)
    
    def drawGrid(self) -> None:
        for i in range(-self.grid_size,self.grid_size+1):
            line = QGraphicsLineItem()
            if i%2 == 0: line.setPen(self.grid_pen_bold)
            else: line.setPen(self.grid_pen)
            line.setLine(0,0,2*self.real_grid_radius,0)
            line.setPos(-self.real_grid_radius,i*self.grid_offset)
            self.addItem(line)
        for i in range(-self.grid_size,self.grid_size+1):
            line = QGraphicsLineItem()
            if i%2 == 0: line.setPen(self.grid_pen_bold)
            else: line.setPen(self.grid_pen)
            line.setLine(0,0,0,2*self.real_grid_radius)
            line.setPos(i*self.grid_offset,-self.real_grid_radius)
            self.addItem(line)
    
    def computeDefaultCoords(self) -> None:
        self.circuit.updateDepth()
        self.nb_cols = self.circuit.depth+1

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