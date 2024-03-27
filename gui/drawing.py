from tkinter import *
from engine import *
import math

config = {
    "gatewidth": 20,
    "yoffset": 40,
    "xoffset": 50,
    "dividersize": 13,
    "padding": 70,
    "controlradius": 3,
    "targetradius": 6
}

class CircuitDrawing:
    def __init__(self, canvas, circuit) -> None:
        self.canvas = canvas
        self.circuit = circuit

        self.nbcols = None
        self.nbrows = None
        self.truex = None
        self.truey = None
        self.computeDimensions()
        self.computeGrid()
        self.computeTrueCoordinates()

        self.drawBackgroundLines()
        self.drawCircuit()
        # self.drawIds()
        # self.drawInputs()

    def computeDimensions(self) -> None:
        # compute x dimension and true x coordinates
        self.nbcols = 0
        for gate in self.circuit.gates:
            x,y = gate.pos
            self.nbcols = max(self.nbcols, x+1)

        # compute y dimensions
        self.divsAndGaths = [[] for i in range(self.nbcols)]
        for gate in self.circuit.gates:
            if gate.type == "D" or gate.type == "G":
                x,y = gate.pos
                self.divsAndGaths[x].append(gate)
        self.nbrows = [0 for i in range(self.nbcols)]
        self.nbrows[0] = len(self.circuit.org)
        for x in range(1,self.nbcols):
            self.nbrows[x] += self.nbrows[x-1]
            for dg in self.divsAndGaths[x]:
                if dg.type == "D": self.nbrows[x+1] += 1
                elif dg.type == "G": self.nbrows[x+1] -= 1
    
    def computeGrid(self) -> None:
        # self.grid[i][j] contains the gate id at position (i,j)
        self.grid = [[None for j in range(self.nbrows[i])] for i in range(self.nbcols)]
        for gate in self.circuit.gates:
            x,y = gate.pos
            if type(y) == int:
                self.grid[x][y] = gate.id
            else:
                for i in y: self.grid[x][i] = gate.id
    
    def computeTrueCoordinates(self) -> None:
        # compute true x coordinates
        self.truex = [config["padding"] + config["xoffset"]*i for i in range(self.nbcols)]

        # compute true y coordinates
        self.truey = [[None for j in range(self.nbrows[i])] for i in range(self.nbcols)]
        previousOutputs = [config["padding"]+i*config["yoffset"] for i in range(self.nbrows[0])]
        self.truey[0] = previousOutputs.copy()
        for i in range(1,self.nbcols):
            nextOutputs = []
            for j in range(self.nbrows[i]):
                # if y is the second input of a gather
                if j>0 and self.grid[i][j-1] != None and self.circuit.gates[self.grid[i][j-1]].type == "G":
                    self.truey[i][j] = previousOutputs.pop(0)
                else:
                    self.truey[i][j] = previousOutputs.pop(0)
                    if self.grid[i][j] == None:
                        nextOutputs.append(self.truey[i][j])
                    else:
                        gate = self.circuit.gates[self.grid[i][j]]
                        if gate.type == "D":
                            top = 999
                            bottom = 999
                            if j>0: top = self.truey[i][j]-self.truey[i][j-1]
                            if j+1<self.nbrows[i]: bottom = previousOutputs[0]-self.truey[i][j]
                            width = min(top, bottom)*2/3
                            nextOutputs.append(self.truey[i][j]-width/2)
                            nextOutputs.append(self.truey[i][j]+width/2)
                        elif gate.type == "G":
                            nextOutputs.append((self.truey[i][j]+previousOutputs[0])/2)
                        else:
                            nextOutputs.append(self.truey[i][j])
            previousOutputs = nextOutputs

    def x(self, i) -> int:
        return self.truex[i]
    
    def y(self, x, i) -> int:
        return self.truey[x][i]

    def drawBackgroundLines(self):
        # draw vertical lines
        for i in range(len(self.truex)):
            self.canvas.create_line(self.x(i),0,self.x(i),self.canvas.cget('height'), width=1, fill="#ffdddd", dash=(3,3))
        # draw horizontal lines
        for j in range(len(self.truey[0])):
            self.canvas.create_line(0,self.y(0,j),self.x(0),self.y(0,j), width=1, fill="#ffdddd", dash=(3,3))
        for i in range(1,len(self.truex)):
            for j in range(len(self.truey[i])):
                self.canvas.create_line(self.x(i-1),self.y(i,j),self.x(i),self.y(i,j), width=1, fill="#ffdddd", dash=(3,3))
        for j in range(len(self.truey[-1])):
            self.canvas.create_line(self.x(-1),self.y(-1,j),self.canvas.cget('width'),self.y(-1,j), width=1, fill="#ffdddd", dash=(3,3))

    def drawIds(self) -> None:
        for gate in self.circuit.gates:
            x,y = gate.pos
            if type(y)==int: y = [y]
            self.canvas.create_text(self.x(x), self.y(x,y[0])-9, fill="#0000ff", text=str(gate.id))

    def drawInputs(self) -> None:
        for gate in self.circuit.gates:
            x,y = gate.pos
            if type(y)==int: y = [y]
            for qubit in range(len(y)):
                self.canvas.create_text(self.x(x)-14, self.y(x,y[qubit]), fill="green", text=str(qubit))

    def bound(self, x, y) -> None:
        x1 = self.x(x)-2
        y1 = self.y(x,y)-2
        x2 = self.x(x)+2
        y2 = self.y(x,y)+2
        self.canvas.create_rectangle(x1,y1,x2,y2, outline="black", fill="black", width=1)

    def gate(self, gate) -> None:
        x,y = gate.pos
        if type(y) == int: y = [y]
        ysorted = sorted([(y[qubit],qubit) for qubit in range(len(y))], key=lambda x: x[0])
        
        self.canvas.create_line(self.x(x),self.y(x,ysorted[0][0]),self.x(x),self.y(x,ysorted[-1][0]), width=1, fill="black")
        t,b = 0,0
        while b<=len(y)-1:
            last = t
            while b<len(y)-1 and ysorted[b+1][0]-ysorted[b][0]<=1:
                b += 1
            x1 = self.x(x)-config["gatewidth"]/2
            y1 = self.y(x,ysorted[t][0])-config["gatewidth"]/2
            x2 = self.x(x)+config["gatewidth"]/2
            y2 = self.y(x,ysorted[b][0])+config["gatewidth"]/2
            self.canvas.create_rectangle(x1,y1,x2,y2, outline="black", fill="white", width=1)
            self.canvas.create_text(self.x(x), (self.y(x,ysorted[t][0])+self.y(x,ysorted[b][0]))/2, fill="black", text=gate.type)
            b += 1
            t = b
            
    def cnot(self, gate) -> None:
        x,y = gate.pos
        xcontrol,ycontrol = self.x(x),self.y(x,y[0])
        xtarget,ytarget = self.x(x),self.y(x,y[1])
        self.canvas.create_oval(xcontrol-config["controlradius"],ycontrol-config["controlradius"],xcontrol+config["controlradius"],ycontrol+config["controlradius"], outline = "black", fill = "black", width =1)
        self.canvas.create_oval(xtarget-config["targetradius"],ytarget-config["targetradius"],xtarget+config["targetradius"],ytarget+config["targetradius"], outline = "black", fill = "", width = 1)
        ytargetline = ytarget+config["targetradius"]
        if self.y(x,y[0])>self.y(x,y[1]): ytargetline = ytarget-config["targetradius"]
        self.canvas.create_line(xcontrol, ycontrol, xtarget, ytargetline, width =1, fill = "black")
        self.canvas.create_line(xtarget-config["targetradius"], ytarget, xtarget+config["targetradius"], ytarget, width =1, fill = "black")

    def divider(self, x, y) -> None:
        x1 = self.x(x)-config["dividersize"]*math.sqrt(3)/2
        y1 = self.y(x,y)
        x2 = self.x(x)
        y2 = self.y(x,y)-config["dividersize"]/2
        x3 = self.x(x)
        y3 = self.y(x,y)+config["dividersize"]/2
        self.canvas.create_polygon((x1,y1,x2,y2,x3,y3), width =1, outline="black", fill="grey")
        
    def gatherer(self, x, y) -> None:
        x1 = self.x(x)+config["dividersize"]*math.sqrt(3)/2
        y1 = (self.y(x,y)+self.y(x,y+1))/2
        x2 = self.x(x)
        y2 = y1-config["dividersize"]/2
        x3 = self.x(x)
        y3 = y1+config["dividersize"]/2
        self.canvas.create_polygon((x1,y1,x2,y2,x3,y3), width =1, outline="black", fill="grey")
        
    def drawCircuit(self):
        # draw wires
        queue = self.circuit.org.copy()
        visited = [False for i in range(len(self.circuit.gates))]
        while len(queue)>0:
            currentid = queue.pop(0)
            currentgate = self.circuit.gates[currentid]
            x,y = currentgate.pos
            if type(y) == int: y = [y]
            for (idpred,wiring) in currentgate.preset:
                gatepred = self.circuit.gates[idpred]
                xpred,ypred = gatepred.pos
                if type(ypred) == int: ypred = [ypred]
                if gatepred.type == "D" or gatepred.type == "G":
                    self.canvas.create_line(self.x(xpred),self.y(x,y[wiring[1]]),self.x(x),self.y(x,y[wiring[1]]), fill="black", width=1)
                else:
                    if currentgate.type == "G":
                        self.canvas.create_line(self.x(xpred),self.y(xpred,ypred[wiring[0]]),self.x(x),self.y(xpred,ypred[wiring[0]]), fill="black", width=1)
                        pass
                    else:
                        self.canvas.create_line(self.x(xpred),self.y(xpred,ypred[wiring[0]]),self.x(x),self.y(x,y[wiring[1]]), fill="black", width=1)
            for (idsucc,wiring) in currentgate.postset:
                if not visited[idsucc]:
                    queue.append(idsucc)
                    visited[idsucc] = True

        # draw gates
        for i in range(len(self.circuit.gates)):
            gate = self.circuit.gates[i]
            x,y = gate.pos
            if gate.type == "in" or gate.type == "out":
                self.bound(x,y)
            elif gate.type == "CNOT":
                self.cnot(gate)
            elif gate.type == "D":
                self.divider(x,y)
            elif gate.type == "G":
                self.gatherer(x,y)
            else:
                self.gate(gate)
            
            if gate.type == "D":
                succ0 = self.circuit.gates[gate.postset[0][0]]
                wiring0 = gate.postset[0][1]
                succ1 = self.circuit.gates[gate.postset[1][0]]
                wiring1 = gate.postset[1][1]
                xsucc0,ysucc0 = succ0.pos
                if type(ysucc0) == int: ysucc0 = [ysucc0]
                xsucc1,ysucc1 = succ1.pos
                if type(ysucc1) == int: ysucc1 = [ysucc1]
                self.canvas.create_line(self.x(x),self.y(xsucc0,ysucc0[wiring0[1]]),self.x(x),self.y(xsucc1,ysucc1[wiring1[1]]), fill="black", width=1)
            elif gate.type == "G":
                self.canvas.create_line(self.x(x),self.y(x,y),self.x(x),self.y(x,y+1), fill="black", width=1)