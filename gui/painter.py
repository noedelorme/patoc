from tkinter import *
from engine import *

class DagPainter:
    def __init__(self, grid, config) -> None:
        pass


class CircuitPainter:
    def __init__(self, canvas, circuit, config) -> None:
        self.canvas = canvas
        self.circuit = circuit
        self.circuitlenght = 350
        self.boxheight = 20
        self.wireheight = 25
        self.layerwidth = 50
        self.dividerHeight = 12
        self.layerradius = 25
        self.p = 50


        self.xs = [self.p + self.layerwidth*i for i in range(len(circuit.layers))]
        self.ys = [[self.p + self.wireheight*j for j in range(len(layer))] for layer in circuit.layers] # pas tout à fait ça car un cnot prend deux place dans circuit.layer

        self.ys = [
            [25,62,100],
            [25,62,100],
            [25,62,100],
            [25,62,100],
            [25,62,100],
            [25,50,75,100],
            [25,50,75,100]
        ]

        self.grid(7)


        self.box(0,0, "H")
        self.box(1,1, "H")
        self.box(3,1, "H")
        self.box(6,1, "H")
        self.box(1,2, "H")

        self.wire(1,0)
        self.wire(2,2)
        self.wire(3,0)
        self.wire(3,2)
        self.wire(4,0)
        self.wire(4,2)
        self.wire(5,0)
        self.wire(5,1)
        self.wire(5,2)
        self.wire(5,3)
        self.wire(6,0)

        self.cnot(2,0)
        self.cnot(0,1)
        self.cnot(6,2)

        self.divider(4,1)

        


    def grid(self, col):
        for x in self.xs:
            self.canvas.create_line(x,0,x,self.ys[0][-1]+self.wireheight, width=1, fill="gold", dash=(3,3))

    def wire(self, x, y) -> None:
        if x == 0:
            self.canvas.create_line(self.xs[x]-self.layerradius,self.ys[x][y],(self.xs[x]+self.xs[x+1])/2,self.ys[x][y], width=1)
        elif x == len(self.xs)-1:
            self.canvas.create_line((self.xs[x-1]+self.xs[x])/2,self.ys[x][y],self.xs[x]+self.layerradius,self.ys[x][y], width=1)
        else:
            self.canvas.create_line((self.xs[x-1]+self.xs[x])/2,self.ys[x][y],(self.xs[x]+self.xs[x+1])/2,self.ys[x][y], width=1)

    def box(self, x, y, text) -> None:
        self.wire(x,y)
        
        x1 = self.xs[x]-self.boxheight/2
        y1 = self.ys[x][y]-self.boxheight/2
        x2 = self.xs[x]+self.boxheight/2
        y2 = self.ys[x][y]+self.boxheight/2
        self.canvas.create_rectangle(x1,y1,x2,y2, outline="black", fill="white", width = 1)
        self.canvas.create_text(self.xs[x], self.ys[x][y], fill="black", text=text)

    def cnot(self, x, y) -> None:
        """todo: reverse cnot"""
        self.wire(x,y)
        self.wire(x,y+1)

        controlradius = 3
        targetradius = 6
        control_x1 = self.xs[x]-controlradius
        control_y1 = self.ys[x][y]-controlradius
        control_x2 = self.xs[x]+controlradius
        control_y2 = self.ys[x][y]+controlradius
        target_x1 = self.xs[x]-targetradius
        target_y1 = self.ys[x][y+1]-targetradius
        target_x2 = self.xs[x]+targetradius
        target_y2 = self.ys[x][y+1]+targetradius
        self.canvas.create_oval(control_x1,control_y1,control_x2,control_y2, outline = "white", fill = "white", width = 1)
        self.canvas.create_oval(target_x1,target_y1,target_x2,target_y2, outline = "white", fill = "black", width = 1)
        self.canvas.create_line(self.xs[x], self.ys[x][y], self.xs[x], self.ys[x][y+1]+targetradius, width=1)
        self.canvas.create_line(self.xs[x]-targetradius, self.ys[x][y+1], self.xs[x]+targetradius, self.ys[x][y+1], width=1)

    def divider(self, x, y) -> None:
        x1 = self.xs[x]-self.dividerHeight
        y1 = self.ys[x][y]
        x2 = self.xs[x]
        y2 = self.ys[x][y]-self.dividerHeight/2
        x3 = self.xs[x]
        y3 = self.ys[x][y]+self.dividerHeight/2
        self.canvas.create_polygon((x1,y1,x2,y2,x3,y3), fill="white")

        if x == 0:
            self.canvas.create_line(self.xs[x]-self.layerradius,self.ys[x][y],self.xs[x],self.ys[x][y], width=1)
        else:
            self.canvas.create_line((self.xs[x-1]+self.xs[x])/2,self.ys[x][y],self.xs[x],self.ys[x][y], width=1)

        if x == len(self.xs)-1:
            self.canvas.create_line(x2,y2,x2+self.layerradius/3,self.ys[x][y]-self.wireheight/2,x2+self.layerradius,self.ys[x][y]-self.wireheight/2, width=1, smooth=1)
            self.canvas.create_line(x3,y3,x3+self.layerradius/3,self.ys[x][y]+self.wireheight/2,x3+self.layerradius,self.ys[x][y]+self.wireheight/2, width=1, smooth=1)
        else:
            self.canvas.create_line(x2,y2,x2+(self.xs[x+1]-self.xs[x])/2/3,self.ys[x][y]-self.wireheight/2,x2+(self.xs[x+1]-self.xs[x])/2,self.ys[x][y]-self.wireheight/2, width=1, smooth=1)
            self.canvas.create_line(x3,y3,x3+(self.xs[x+1]-self.xs[x])/2/3,self.ys[x][y]+self.wireheight/2,x3+(self.xs[x+1]-self.xs[x])/2,self.ys[x][y]+self.wireheight/2, width=1, smooth=1)
    
    def computeWireHeights(self) -> None:
        pass
        
    def drawCircuit(self):
        for i in range(len(self.circuit.layers)):
            layer = self.circuit.layers[i]
            for j in range(len(layer)):
                if layer[j] == None:
                    self.wire(i,j)
                else:
                    gate = self.circuit.gates[layer[j]]
                    if type(gate) == H:
                        self.box(i,j,"H")
                    elif type(gate) == CNOT:
                        self.cnot(i,j)





# class CircuitPainter:
#     def __init__(self, canvas, config) -> None:
#         self.canvas = canvas
#         self.circuitlenght = 350
#         self.boxheight = 20

#         self.e = 12 # cell size 
#         self.p = 25 # padding 

#         self.controlradius = 3
#         self.targetradius = 6

#         self.box(4,0,"H")
#         self.box(8,3,"H")
#         self.box(16,3,"H")
#         self.box(22,2,"H")
#         self.box(8,6,"H")

        

#         # self.canvas.create_line(150,0, 100,50, 50,0, 0,50, smooth=1) # create a curved line

#     def ports(self, circuit, id) -> tuple[list[tuple[int]],list[tuple[int]]]:
#         """Return the input and output list of coordinates of the ports of a given gate"""
#         gate = circuit.gates[id]
#         if gate.type == "H":
#             x = gate.pos[0][0]
#             y = gate.pos[0][1]
#             input = (x-self.boxheight/2,y)
#             output = (x+self.boxheight/2,y)
#             return ([input],[output])
#         if gate.type == "CX":
#             input_c = (gate.pos[0][0]-self.controlradius/2,gate.pos[0][1])
#             output_c = (gate.pos[0][0]+self.controlradius/2,gate.pos[0][1])
#             input_t = (gate.pos[1][0]-self.targetradius/2,gate.pos[1][1])
#             output_t = (gate.pos[1][0]+self.targetradius/2,gate.pos[1][1])
#             return ([input_c,input_t],[output_c,output_t])

#     def grid(self, col):
#         for i in range(1,col):
#             self.canvas.create_line(i*self.layerwidth,0,i*self.layerwidth,100, width=1, fill="gold", dash=(3,5))

#     def wire(self, circuit, id1, id2, output1, input2) -> None:
#         port1 = self.ports(circuit, id1)[1][output1]
#         port2 = self.ports(circuit, id2)[0][input2]
#         x1 = port1[0]
#         y1 = port1[1]
#         x2 = port2[0]
#         y2 = port2[1]
#         self.canvas.create_line(x1,y1,x2,y2, width=1)

#     def box(self, x, y, text) -> None:
#         boxradius = 10
#         x1 = x*self.e-self.boxheight/2
#         y1 = y*self.e-self.boxheight/2
#         x2 = x*self.e+self.boxheight/2
#         y2 = y*self.e+self.boxheight/2
#         self.canvas.create_rectangle(self.p+x1,self.p+y1,self.p+x2,self.p+y2, outline="black", fill="white", width = 1)
#         self.canvas.create_text(self.p+x*self.e, self.p+y*self.e, fill="black", text=text)

#     def cnot(self, x, y) -> None:
#         """todo: reverse cnot"""
#         controlradius = 3
#         targetradius = 6
#         control_x1 = x*self.layerwidth-controlradius
#         control_y1 = y*self.wireheight-controlradius
#         control_x2 = x*self.layerwidth+controlradius
#         control_y2 = y*self.wireheight+controlradius
#         target_x1 = x*self.layerwidth-targetradius
#         target_y1 = (y+1)*self.wireheight-targetradius
#         target_x2 = x*self.layerwidth+targetradius
#         target_y2 = (y+1)*self.wireheight+targetradius
#         self.canvas.create_oval(control_x1,control_y1,control_x2,control_y2, outline = "white", fill = "white", width = 1)
#         self.canvas.create_oval(target_x1,target_y1,target_x2,target_y2, outline = "white", fill = "black", width = 1)
#         self.canvas.create_line(x*self.layerwidth, y*self.wireheight, x*self.layerwidth, (y+1)*self.wireheight+targetradius, width=1)
#         self.canvas.create_line(x*self.layerwidth-targetradius, (y+1)*self.wireheight, x*self.layerwidth+targetradius, (y+1)*self.wireheight, width=1)

#     def divider(self, x, y) -> None:
#         dividerHeight = 12
#         x1 = x*self.layerwidth-dividerHeight/2
#         y1 = y*self.wireheight
#         x2 = x*self.layerwidth+dividerHeight/2
#         y2 = y*self.wireheight-dividerHeight/2
#         x3 = x*self.layerwidth+dividerHeight/2
#         y3 = y*self.wireheight+dividerHeight/2
#         self.canvas.create_polygon((x1,y1,x2,y2,x3,y3), fill="white")
