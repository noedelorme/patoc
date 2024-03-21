from tkinter import *
from engine import *

class CircuitDrawing:
    def __init__(self, canvas, circuit, config) -> None:
        self.canvas = canvas
        self.circuit = circuit
        self.circuitlenght = 350
        self.boxheight = 20
        self.wireheight = 40
        self.deflayerwidth = 50
        self.dividerHeight = 13
        self.layerradius = 25
        self.p = 70

        self.truex = None
        self.truey = None
        self.nbrows = None
        self.nbcols = None

        self.computeDimensions()
        self.computeGrid()
        self.computeTrueCoordinates()

        self.drawBackgroundLines()
        # self.drawCircuit()
        # self.drawIds()


        e = Gate(0,"E", arity=3, pos=(3,0))
        cx = Gate(0,"CNOT", pos=(4,[0,1]))
        f = Gate(0,"F", pos=(4,2))
        h = Gate(0,"H", arity=4, pos=(0,[2,3,4,5]))
        j = Gate(0,"J", arity=3, pos=(1,[2,4,5]))
        k = Gate(0,"K", arity=3, pos=(3,[2,3,5]))
        self.gate(e)
        self.gate(cx)
        self.gate(f)
        self.gate(h)
        self.gate(j)
        self.gate(k)


    
    def computeDimensions(self) -> None:
        # compute x dimension and true x coordinates
        self.nbcols = 0
        for gate in self.circuit.gates:
            x,y = gate.pos
            self.nbcols = max(self.nbcols, x+1)

        # compute y dimensions
        self.divsAndGaths = [[] for i in range(self.nbcols)] # list of list of dividers and gatherers in each col
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
        self.truex = [self.p + self.deflayerwidth*i for i in range(self.nbcols)]

        # compute true y coordinates
        self.truey = [[None for j in range(self.nbrows[i])] for i in range(self.nbcols)]
        previousOutputs = [self.p+i*self.wireheight for i in range(self.nbrows[0])]
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
            self.canvas.create_text(self.x(x)-9, self.y(x,y), fill="#0000ff", text=str(gate.id))
    
    def wire(self, x, y) -> None:
        if x == 0:
            self.canvas.create_line(self.xs[x]-self.layerradius,self.ys[x][y],(self.xs[x]+self.xs[x+1])/2,self.ys[x][y], fill="black", width =1)
        elif x == len(self.xs)-1:
            self.canvas.create_line((self.xs[x-1]+self.xs[x])/2,self.ys[x][y],self.xs[x]+self.layerradius,self.ys[x][y], fill="black", width =1)
        else:
            self.canvas.create_line((self.xs[x-1]+self.xs[x])/2,self.ys[x][y],(self.xs[x]+self.xs[x+1])/2,self.ys[x][y], fill="black", width =1)

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
        print(ysorted)
        while b<=len(y)-1:
            last = t
            while b<len(y)-1 and ysorted[b+1][0]-ysorted[b][0]<=1:
                b += 1
            print(t,b)
            x1 = self.x(x)-self.boxheight/2
            y1 = self.y(x,ysorted[t][0])-self.boxheight/2
            x2 = self.x(x)+self.boxheight/2
            y2 = self.y(x,ysorted[b][0])+self.boxheight/2
            self.canvas.create_rectangle(x1,y1,x2,y2, outline="black", fill="white", width=1)
            self.canvas.create_text(self.x(x), (self.y(x,ysorted[t][0])+self.y(x,ysorted[b][0]))/2, fill="black", text=gate.type)
            b += 1
            t = b

        for qubit in range(len(y)):
            self.canvas.create_text(self.x(x)-14, self.y(x,y[qubit]), fill="green", text=str(qubit))

    def cnot(self, x, y) -> None:
        """todo: reverse cnot"""
        # self.wire(x,y)
        # self.wire(x,y+1)

        controlradius = 3
        targetradius = 6
        control_x1 = self.x(x)-controlradius
        control_y1 = self.y(x,y)-controlradius
        control_x2 = self.x(x)+controlradius
        control_y2 = self.y(x,y)+controlradius
        target_x1 = self.x(x)-targetradius
        target_y1 = self.y(x,y+1)-targetradius
        target_x2 = self.x(x)+targetradius
        target_y2 = self.y(x,y+1)+targetradius
        self.canvas.create_oval(control_x1,control_y1,control_x2,control_y2, outline = "black", fill = "black", width =1)
        self.canvas.create_oval(target_x1,target_y1,target_x2,target_y2, outline = "black", fill = "", width = 1)
        self.canvas.create_line(self.x(x), self.y(x,y), self.x(x), self.y(x,y+1)+targetradius, width =1, fill = "black")
        self.canvas.create_line(self.x(x)-targetradius, self.y(x,y+1), self.x(x)+targetradius, self.y(x,y+1), width =1, fill = "black")

    def divider(self, x, y) -> None:
        x1 = self.x(x)-self.dividerHeight
        y1 = self.y(x,y)
        x2 = self.x(x)
        y2 = self.y(x,y)-self.dividerHeight/2
        x3 = self.x(x)
        y3 = self.y(x,y)+self.dividerHeight/2
        self.canvas.create_polygon((x1,y1,x2,y2,x3,y3), width =1, outline="black", fill="grey")

        # if x == 0:
        #     self.canvas.create_line(x1-self.layerradius,self.ys[x][y],x1,self.ys[x][y], fill="black", width =1)
        # else:
        #     self.canvas.create_line((self.xs[x-1]+x1)/2,self.ys[x][y],x1,self.ys[x][y], fill="black", width =1)

        # if x == len(self.xs)-1:
        #     self.canvas.create_line(x2,y2,x2+self.layerradius/3,self.ys[x][y]-self.wireheight/2,x2+self.layerradius,self.ys[x][y]-self.wireheight/2, fill="black", width =1, smooth=1)
        #     self.canvas.create_line(x3,y3,x3+self.layerradius/3,self.ys[x][y]+self.wireheight/2,x3+self.layerradius,self.ys[x][y]+self.wireheight/2, fill="black", width =1, smooth=1)
        # else:
        #     self.canvas.create_line(x2,y2,x2+(self.xs[x+1]-self.xs[x])/2/3,self.ys[x][y]-self.wireheight/2,x2+(self.xs[x+1]-self.xs[x])/2,self.ys[x][y]-self.wireheight/2, fill="black", width =1, smooth=1)
        #     self.canvas.create_line(x3,y3,x3+(self.xs[x+1]-self.xs[x])/2/3,self.ys[x][y]+self.wireheight/2,x3+(self.xs[x+1]-self.xs[x])/2,self.ys[x][y]+self.wireheight/2, fill="black", width =1, smooth=1)
        
    def gatherer(self, x, y) -> None:
        x1 = self.x(x)+self.dividerHeight
        y1 = (self.y(x,y)+self.y(x,y+1))/2
        x2 = self.x(x)
        y2 = y1-self.dividerHeight/2
        x3 = self.x(x)
        y3 = y1+self.dividerHeight/2
        self.canvas.create_polygon((x1,y1,x2,y2,x3,y3), width =1, outline="black", fill="grey")

        # # draw top input wire
        # ##########################################
        # self.canvas.create_line(x2-(self.xs[x]-self.xs[x-1])/2,self.ys[x][y]-self.wireheight/2,
        #                         x2-(self.xs[x]-self.xs[x-1])/2/3,self.ys[x][y]-self.wireheight/2,
        #                         x2,y2, fill="black", width=1, smooth=1)
        # # draw bottom input wire 
        # self.canvas.create_line(x2-(self.xs[x]-self.xs[x-1])/2,self.ys[x][y]+self.wireheight/2,x2-(self.xs[x]-self.xs[x-1])/2/3,self.ys[x][y]+self.wireheight/2,x3,y3, fill="black", width=1, smooth=1)
        # # draw single output wire 
        # self.canvas.create_line(x1,self.ys[x][y],(self.xs[x]+self.xs[x+1])/2,self.ys[x][y], fill="black", width=1)

    def drawGate(self, id) -> None:
        gate = self.circuit.gates[id]
        x,y = gate.pos
        if gate.type == "in" or gate.type == "out":
            self.bound(x,y)
        elif gate.type == "H":
            self.box(x,y,gate.dom,"H")
        elif gate.type == "CNOT":
            self.cnot(x,y)
        elif gate.type == "D":
            self.divider(x,y)
        elif gate.type == "G":
            self.gatherer(x,y)
        else:
            self.box(x,y,gate.dom,gate.type)
        
    def drawCircuit(self):
        # draw wires
        queue = self.circuit.org.copy()
        visited = [False for i in range(len(self.circuit.gates))]
        while len(queue)>0:
            currentid = queue.pop(0)
            currentgate = self.circuit.gates[currentid]
            x,y = currentgate.pos
            for (idpred,wiring) in currentgate.preset:
                gatepred = self.circuit.gates[idpred]
                xpred,ypred = gatepred.pos
                if gatepred.type == "D" or gatepred.type == "G":
                    self.canvas.create_line(self.x(xpred),self.y(x,y+wiring[1]),self.x(x),self.y(x,y+wiring[1]), fill="black", width=1)
                else:
                    self.canvas.create_line(self.x(xpred),self.y(xpred,ypred+wiring[0]),self.x(x),self.y(x,y+wiring[1]), fill="black", width=1)
            for (idsucc,wiring) in currentgate.postset:
                if not visited[idsucc]:
                    queue.append(idsucc)
                    visited[idsucc] = True

        # draw gates
        for i in range(len(self.circuit.gates)):
            self.drawGate(i)
            gate = self.circuit.gates[i]
            x,y = gate.pos
            if gate.type == "D":
                succ0 = self.circuit.gates[gate.postset[0][0]]
                succ1 = self.circuit.gates[gate.postset[1][0]]
                xsucc0,ysucc0 = succ0.pos
                xsucc1,ysucc1 = succ1.pos
                self.canvas.create_line(self.x(x),self.y(xsucc0,ysucc0),self.x(x),self.y(xsucc1,ysucc1), fill="black", width=1)
            elif gate.type == "G":
                self.canvas.create_line(self.x(x),self.y(x,y),self.x(x),self.y(x,y+1), fill="black", width=1)