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
        self.p = 50

        # self.truex = [self.p + self.deflayerwidth*i for i in range(circuit.nblayers)]
        # self.truey = [
        #     [self.p+25,self.p+62,self.p+100,self.p+125],
        #     [self.p+25,self.p+62,self.p+100,self.p+125],
        #     [self.p+25,self.p+62,self.p+100,self.p+125],
        #     [self.p+25,self.p+62,self.p+100,self.p+125],
        #     [self.p+25,self.p+62,self.p+100,self.p+125],
        #     [self.p+25,self.p+62,self.p+100,self.p+125],
        #     [self.p+25,self.p+50,self.p+75,self.p+100,self.p+125],
        #     [self.p+25,self.p+50,self.p+75,self.p+100,self.p+125],
        #     [self.p+25,self.p+50,self.p+75,self.p+100,self.p+125],
        #     [self.p+37,self.p+75,self.p+100,self.p+125],
        #     [self.p+56,self.p+100,self.p+125]
        # ]

        self.truex = None
        self.truey = None
        # self.computeTrueCoords()



        # compute x dimension and true coordinates
        nbcols = 0
        for gate in self.circuit.gates:
            x,y = gate.pos
            nbcols = max(nbcols, x+1)
        self.truex = [self.p + self.deflayerwidth*i for i in range(nbcols)]

        # compute y dimensions and naive true coordinates
        self.divsAndGaths = [[] for i in range(nbcols)] # list of list of dividers and gatherers in each col
        for gate in self.circuit.gates:
            if gate.type == "D" or gate.type == "G":
                x,y = gate.pos
                self.divsAndGaths[x].append(gate)
        
        nbrows = [0 for i in range(nbcols)]
        nbrows[0] = len(self.circuit.org)
        for x in range(1,nbcols):
            nbrows[x] += nbrows[x-1]
            for dg in self.divsAndGaths[x]:
                if dg.type == "D": nbrows[x+1] += 1
                elif dg.type == "G": nbrows[x+1] -= 1
        # self.truey = [[self.p+j*self.wireheight for j in range(nbrows[i])] for i in range(nbcols)]

        grid = [[None for j in range(nbrows[i])] for i in range(nbcols)]
        for gate in self.circuit.gates:
            x,y = gate.pos
            grid[x][y] = gate.id


        print(nbcols, nbrows)
        self.truey = [[None for j in range(nbrows[i])] for i in range(nbcols)]
        # previousOutputs = [self.p,self.p+100,self.p+200,self.p+250]
        previousOutputs = [self.p+i*self.wireheight for i in range(nbrows[0])]
        self.truey[0] = previousOutputs.copy()
        for i in range(1,nbcols):
            nextOutputs = []
            for j in range(nbrows[i]):
                # if y is the second input of a gather
                if j>0 and grid[i][j-1] != None and self.circuit.gates[grid[i][j-1]].type == "G":
                    print("merdouille")
                    self.truey[i][j] = previousOutputs.pop(0)
                else:
                    self.truey[i][j] = previousOutputs.pop(0)
                    if grid[i][j] == None:
                        nextOutputs.append(self.truey[i][j])
                    else:
                        gate = self.circuit.gates[grid[i][j]]
                        if gate.type == "D":
                            top = 999
                            bottom = 999
                            if j>0: top = self.truey[i][j]-self.truey[i][j-1]
                            if j+1<nbrows[i]: bottom = previousOutputs[0]-self.truey[i][j]
                            width = min(top, bottom)*2/3
                            nextOutputs.append(self.truey[i][j]-width/2)
                            nextOutputs.append(self.truey[i][j]+width/2)
                        elif gate.type == "G":
                            nextOutputs.append((self.truey[i][j]+previousOutputs[0])/2)
                        else:
                            nextOutputs.append(self.truey[i][j])
            previousOutputs = nextOutputs


        self.drawGrid()
        self.drawCircuit()
        self.drawIds()
    
    def liftDivider(self,x,y,amount) -> None:
        """Push down all the coords that are affected by pushing down (x,y)"""
        self.truey[x][y] += amount

        # push down every coords bellow and right of x,y (y layer included)
        for i in range(x,-1,-1):
            layer = self.truey[i]
            print(len(self.divsAndGaths[i]))
            if len(self.divsAndGaths[i])==0: # if there is no divider in the layer
                for yi in range(y,len(layer)):
                    self.truey[i][yi] += amount
            else:
                pass

        # push down every coords bellow and left of x,y
        for i in range(x+1,self.nbcols):
            layer = self.truey[i]
            if len(self.divsAndGaths[i])==0: # if there is no divider in the layer
                for yi in range(y,len(layer)):
                    self.truey[i][yi] += amount
            else:
                pass
    
    def computeTrueCoords(self) -> None:
        # compute x dimension and true coordinates
        nbcols = 0
        for gate in self.circuit.gates:
            x,y = gate.pos
            nbcols = max(nbcols, x+1)
        print("test1", nbcols)
        self.truex = [self.p + self.deflayerwidth*i for i in range(nbcols)]

        # compute y dimensions and naive true coordinates
        divsAndGaths = [[] for i in range(nbcols)] # list of list of dividers and gatherers in each col
        for gate in self.circuit.gates:
            if gate.type == "D" or gate.type == "G":
                x,y = gate.pos
                divsAndGaths[x].append(gate)
        
        nbrows = [0 for i in range(nbcols)]
        nbrows[0] = len(self.circuit.org)
        for x in range(1,nbcols):
            if len(divsAndGaths[x])>0:
                nbrow = nbrows[x-1]
                for dg in divsAndGaths[x]:
                    if dg.type == "D": nbrow += 1
                    elif dg.type == "G": nbrow -= 1
                nbrows[x] = nbrow
            else:
                nbrows[x] = nbrows[x-1]
        print("test2", nbrows)
        # self.truey = [[self.p+j*self.wireheight for j in range(nbrows[i])] for i in range(nbcols)]

        grid = [[None for j in range(nbrows[i])] for i in range(nbcols)]
        for gate in self.circuit.gates:
            x,y = gate.pos
            grid[x][y] = gate.id

        print(grid)

        

        # for i in range(1,nbcols):
        #     for dg in divsAndGaths[i]: # for each div or gath in col i



        # queue = self.circuit.org.copy()
        # visited = [False for i in range(len(self.circuit.gates))]
        # for id in queue: visited[id]=True
        # while len(queue)>0:
        #     currentid = queue.pop(0)
        #     currentgate = self.circuit.gates[currentid]
        #     x,y = currentgate.pos
        #     for (idsucc,wiring) in currentgate.postset:
        #         if not visited[idsucc]:
        #             queue.append(idsucc)
        #             visited[idsucc] = True

    def x(self, i) -> int:
        return self.truex[i]
    
    def y(self, x, i) -> int:
        return self.truey[x][i]

    def drawGrid(self):
        for i in range(len(self.truex)):
            self.canvas.create_line(self.x(i),self.y(i,0),self.x(i),self.y(i,-1), width=1, fill="#ffdddd", dash=(3,3))
    
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

    def box(self, x, y, text) -> None:
        x1 = self.x(x)-self.boxheight/2
        y1 = self.y(x,y)-self.boxheight/2
        x2 = self.x(x)+self.boxheight/2
        y2 = self.y(x,y)+self.boxheight/2
        self.canvas.create_rectangle(x1,y1,x2,y2, outline="black", fill="white", width=1)
        self.canvas.create_text(self.x(x), self.y(x,y), fill="black", text=text)

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
        if gate.type == "H":
            self.box(x,y,"H")
        elif gate.type == "CNOT":
            self.cnot(x,y)
        elif gate.type == "D":
            self.divider(x,y)
        elif gate.type == "G":
            self.gatherer(x,y)
        
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
                if gatepred.type == "D":
                    self.canvas.create_line(self.x(xpred),self.y(x,y+wiring[1]),self.x(x),self.y(x,y+wiring[1]), fill="black", width=1)
                elif gatepred.type == "G":
                    self.canvas.create_line(self.x(xpred),self.y(x,y+wiring[1]),self.x(x),self.y(x,y+wiring[1]), fill="black", width=1)
                else:
                    self.canvas.create_line(self.x(xpred),self.y(xpred,ypred+wiring[0]),self.x(x),self.y(x,y+wiring[1]), fill="black", width=1)
            for (idsucc,wiring) in currentgate.postset:
                if not visited[idsucc]:
                    queue.append(idsucc)
                    visited[idsucc] = True

        # draw gates
        for i in range(len(self.circuit.gates)):
            # if self.circuit.gates[i].type == "D" or self.circuit.gates[i].type == "G": #temp
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