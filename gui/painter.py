from tkinter import *

class DagPainter:
    def __init__(self, grid, config) -> None:
        pass

class CircuitPainter:
    def __init__(self, canvas, config) -> None:
        self.canvas = canvas
        self.circuitlenght = 350
        self.boxheight = 20
        self.wireheight = 25
        self.layerwidth = 50

        self.grid(7)

        self.wire(1)
        self.wire(2)
        self.wire(3)

        self.box(1,1, "H")
        self.box(3,2, "H")
        self.box(6,3, "T")

        self.cnot(4,2)

        self.divider(5,2)

        # self.canvas.create_line(150,0, 100,50, 50,0, 0,50, smooth=1) # create a curved line

    def grid(self, col):
        for i in range(1,col):
            self.canvas.create_line(i*self.layerwidth,0,i*self.layerwidth,100, width=1, fill="gold", dash=(3,5))

    def wire(self, y) -> None:
        x1 = 0
        y1 = y*self.wireheight
        x2 = self.circuitlenght
        y2 = y*self.wireheight
        self.canvas.create_line(x1,y1,x2,y2, width=1)

    def box(self, x, y, text) -> None:
        boxradius = 10
        x1 = x*self.layerwidth-self.boxheight/2
        y1 = y*self.wireheight-self.boxheight/2
        x2 = x*self.layerwidth+self.boxheight/2
        y2 = y*self.wireheight+self.boxheight/2
        self.canvas.create_rectangle(x1,y1,x2,y2, outline="black", fill="white", width = 1)
        self.canvas.create_text(x*self.layerwidth, y*self.wireheight, fill="black", text=text)

    def cnot(self, x, y) -> None:
        """todo: reverse cnot"""
        controlradius = 3
        targetradius = 6
        control_x1 = x*self.layerwidth-controlradius
        control_y1 = y*self.wireheight-controlradius
        control_x2 = x*self.layerwidth+controlradius
        control_y2 = y*self.wireheight+controlradius
        target_x1 = x*self.layerwidth-targetradius
        target_y1 = (y+1)*self.wireheight-targetradius
        target_x2 = x*self.layerwidth+targetradius
        target_y2 = (y+1)*self.wireheight+targetradius
        self.canvas.create_oval(control_x1,control_y1,control_x2,control_y2, outline = "white", fill = "white", width = 1)
        self.canvas.create_oval(target_x1,target_y1,target_x2,target_y2, outline = "white", fill = "black", width = 1)
        self.canvas.create_line(x*self.layerwidth, y*self.wireheight, x*self.layerwidth, (y+1)*self.wireheight+targetradius, width=1)
        self.canvas.create_line(x*self.layerwidth-targetradius, (y+1)*self.wireheight, x*self.layerwidth+targetradius, (y+1)*self.wireheight, width=1)

    def divider(self, x, y) -> None:
        dividerHeight = 12
        x1 = x*self.layerwidth-dividerHeight/2
        y1 = y*self.wireheight
        x2 = x*self.layerwidth+dividerHeight/2
        y2 = y*self.wireheight-dividerHeight/2
        x3 = x*self.layerwidth+dividerHeight/2
        y3 = y*self.wireheight+dividerHeight/2
        self.canvas.create_polygon((x1,y1,x2,y2,x3,y3), fill="white")