from engine.circuit import Circuit, Gate

class Grid:
    """Positionning structure for circuits"""

    y_offset = 50
    x_offset = 70

    def __init__(self, circuit: Circuit) -> None:
        self.circuit = circuit
        self.nb_cols = None
        self.nb_rows = None
        self.true_x = None
        self.true_y = None
        self.gates = None

        self.computeDefaultCoords()

        # self.computeDimensions()
        # self.computeGrid()
        # self.computeDefaultTrueCoordinates()

    def computeDefaultCoords(self) -> None:
        self.circuit.updateDepth()
        self.nb_cols = self.circuit.depth+1
        self.nb_rows = [None for i in range(self.nb_cols)]
        self.gates = [[] for i in range(self.nb_cols)]

        def nextWire(x,y):
            layer = self.gates[x]
            wire = 0
            for i in range(y):
                id = layer[i]
                if id == None:
                    wire += 1
                else:
                    gate = self.circuit.gates[id]
                    if gate.type == "D":
                        wire += 2
                    elif gate.type == "G":
                        wire += 0
                    else:
                        wire += 1
            return wire

        # set pos for org boundaries
        for i in range(len(self.circuit.org)):
            id = self.circuit.org[i]
            gate = self.circuit.gates[id]
            self.gates[0].append(id)
            gate.pos = (0,i)
        self.nb_rows[0] = len(self.gates[0])

        for i in range(1,self.nb_cols):
            self.nb_rows[i] = nextWire(i-1,self.nb_rows[i-1]-1)+1
            self.gates[i] = [None for i in range(self.nb_rows[i])]

            pred_layer = self.gates[i-1]
            for j in range(len(pred_layer)):
                id = pred_layer[j]
                if id != None:
                    gate = self.circuit.gates[id]
                    for (id_succ,wiring) in gate.postset:
                        current = self.circuit.gates[id_succ]
                        if current.depth == i:
                            print(gate.type, current.type)
                            y = nextWire(i,j)
                            print(self.gates)
                            current.pos = (i,y)
                            self.gates[i][y] = current.id


        # # first je met toutes les portes dans dans le desordre dans les bonnes layers
        # for gate in self.circuit.gates:
        #     self.gates[gate.depth].append(gate.id)
        
        # for i in range(len(self.gates[0])):
        #     gate = self.circuit.gates[self.gates[0][i]]
        #     gate.pos = (gate.depth,i)




        print(self.gates)

        # def compare(gate_id):
        #     gate = self.circuit.gates[gate_id]
        #     min_y_pred = 99999
        #     for (id_pred,wiring) in gate.preset:
        #         pred = self.circuit.gates[id_pred]
        #         min_y_pred = min(min_y_pred,pred.pos[1])
        #     return min_y_pred

        # for i in range(1,self.nb_cols):
        #     self.gates[i] = sorted(self.gates[i], key=compare)
        
        # print(self.gates)

        # # set pos for org boundaries
        # for i in range(len(self.circuit.org)):
        #     id = self.circuit.org[i]
        #     gate = self.circuit.gates[id]
        #     self.gates[0].append(id)
        #     gate.pos = (0,i)
        # self.nb_rows[0] = len(self.gates[0])



        # used = [False for i in range(len(self.circuit.gates))]
        # for i in range(1,self.nb_cols):
        #     pred_layer = self.gates[i-1]
        #     wire = 0 # number of the wire in the current layer
        #     for j in range(len(pred_layer)): # j is number of the wire in the previous layer
        #         current_pred_id = pred_layer[j]
        #         current_pred = self.circuit.gates[current_pred_id]
        #         if not used[current_pred_id]:
        #             used[current_pred_id] = True
        #             for (id_succ,wiring) in current_pred.postset:
        #                 current = self.circuit.gates[id_succ]
        #                 if current.depth == i:
        #                     self.gates[i].append(id_succ)
        #                 else:
        #                     self.gates[i].append(-1)
        #                 wire += 1


    def x(self, col) -> float:
        return self.true_x[col]
    
    def y(self, col, row) -> float:
        return self.true_y[col][row]

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