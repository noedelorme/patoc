from engine.circuit import Circuit, Gate
from .items import GateItem

class Grid:
    y_offset = 50
    x_offset = 70

    def __init__(self) -> None:
        self.circuit = None
        self.nb_cols = None
        self.nb_rows = None
        self.true_x = None
        self.true_y = None
        self.grid = None

    def x(self, col) -> float:
        return self.true_x[col]
    
    def y(self, col, row) -> float:
        return self.true_y[col][row]
    
    def setCircuit(self, circuit: Circuit) -> None:
        self.circuit = circuit
        self.computeDimensions()
        self.computeGrid()
        self.computeDefaultTrueCoordinates()

    def computeDimensions(self) -> None:
        if self.circuit == None:
            print("No graph specified.")
            return
        
        # compute x dimension
        self.nb_cols = 0
        for gate in self.circuit.gates:
            x,y = gate.pos
            self.nb_cols = max(self.nb_cols, x+1)

        # compute y dimensions
        self.divsAndGaths = [[] for i in range(self.nb_cols)]
        for gate in self.circuit.gates:
            if gate.type == "D" or gate.type == "G":
                x,y = gate.pos
                self.divsAndGaths[x].append(gate)
        self.nb_rows = [0 for i in range(self.nb_cols)]
        self.nb_rows[0] = len(self.circuit.org)
        for x in range(1,self.nb_cols):
            self.nb_rows[x] += self.nb_rows[x-1]
            for dg in self.divsAndGaths[x]:
                if dg.type == "D": self.nb_rows[x+1] += 1
                elif dg.type == "G": self.nb_rows[x+1] -= 1
    
    def computeGrid(self) -> None:
        # self.grid[i][j] contains the gate id at position (i,j)
        self.grid = [[None for j in range(self.nb_rows[i])] for i in range(self.nb_cols)]
        for gate in self.circuit.gates:
            x,y = gate.pos
            if type(y) == int:
                self.grid[x][y] = gate.id
            else:
                for i in y: self.grid[x][i] = gate.id
    
    def computeDefaultTrueCoordinates(self) -> None:
        # compute true x coordinates
        self.true_x = [self.x_offset*i for i in range(self.nb_cols)]

        # compute true y coordinates
        self.true_y = [[None for j in range(self.nb_rows[i])] for i in range(self.nb_cols)]
        previousOutputs = [i*self.y_offset for i in range(self.nb_rows[0])]
        self.true_y[0] = previousOutputs.copy()
        for i in range(1,self.nb_cols):
            nextOutputs = []
            for j in range(self.nb_rows[i]):
                # if y is the second input of a gather
                if j>0 and self.grid[i][j-1] != None and self.circuit.gates[self.grid[i][j-1]].type == "G":
                    self.true_y[i][j] = previousOutputs.pop(0)
                else:
                    self.true_y[i][j] = previousOutputs.pop(0)
                    if self.grid[i][j] == None:
                        nextOutputs.append(self.true_y[i][j])
                    else:
                        gate = self.circuit.gates[self.grid[i][j]]
                        if gate.type == "D":
                            top = 999
                            bottom = 999
                            if j>0: top = self.true_y[i][j]-self.true_y[i][j-1]
                            if j+1<self.nb_rows[i]: bottom = previousOutputs[0]-self.true_y[i][j]
                            width = min(top, bottom)*2/3
                            nextOutputs.append(self.true_y[i][j]-width/2)
                            nextOutputs.append(self.true_y[i][j]+width/2)
                        elif gate.type == "G":
                            nextOutputs.append((self.true_y[i][j]+previousOutputs[0])/2)
                        else:
                            nextOutputs.append(self.true_y[i][j])
            previousOutputs = nextOutputs