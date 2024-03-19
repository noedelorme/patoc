from tkinter import * 
from tkinter.ttk import *
from PIL import Image, ImageTk
from gui.drawing import CircuitDrawing
from engine import *

class MainWindow:
    def __init__(self) -> None:
        root = Tk()
        icon = ImageTk.PhotoImage(Image.open(r"icon.png"))
        root.iconphoto(True, icon)
        root.title("Patoc: a graphical tool for quantum circuits")
        root.config(bg="white")

        org1 = Gate(0,"in", pos=(0,0))
        org2 = Gate(1,"in", pos=(0,1))
        org3 = Gate(2,"in", pos=(0,2))
        org4 = Gate(3,"in", pos=(0,3))
        h1 = Gate(4,"H", pos=(1,0))
        cx1 = Gate(5,"CNOT", pos=(1,1))
        h2 = Gate(6,"H", pos=(2,1))
        h3 = Gate(7,"H", pos=(2,2))
        cx2 = Gate(8,"CNOT", pos=(3,0))
        h4 = Gate(9,"H", pos=(4,1))
        d1 = Gate(10,"D", pos=(5,1))
        h5 = Gate(11,"H", pos=(7,1))
        cx3 = Gate(12,"CNOT", pos=(7,2))
        g1 = Gate(13,"G", pos=(8,0))
        g2 = Gate(14,"G", pos=(9,0))
        dst1 = Gate(15,"out", pos=(10,0))
        dst2 = Gate(16,"out", pos=(10,1))
        dst3 = Gate(17,"out", pos=(10,2))

        circuit = Circuit("cz-one-cnot", [org1,org2,org3,org4,h1,cx1,h2,h3,cx2,h4,d1,h5,cx3,g1,g2,dst1,dst2,dst3],[0,1,2,3],[15,16,17])

        circuit.connect(0, 4, wiring=(0,0))
        circuit.connect(1, 5, wiring=(0,0))
        circuit.connect(2, 5, wiring=(0,1))
        circuit.connect(3, 17, wiring=(0,0))
        circuit.connect(4, 8, wiring=(0,0))
        circuit.connect(5, 6, wiring=(0,0))
        circuit.connect(5, 7, wiring=(1,0))
        circuit.connect(6, 8, wiring=(0,1))
        circuit.connect(7, 12, wiring=(0,1))
        circuit.connect(8, 13, wiring=(0,0))
        circuit.connect(8, 9, wiring=(1,0))
        circuit.connect(9, 10, wiring=(0,0))
        circuit.connect(10, 11, wiring=(0,0))
        circuit.connect(10, 12, wiring=(1,0))
        circuit.connect(11, 13, wiring=(0,1))
        circuit.connect(12, 14, wiring=(0,1))
        circuit.connect(12, 16, wiring=(1,0))
        circuit.connect(13, 14, wiring=(0,0))
        circuit.connect(14, 15, wiring=(0,0))

        # circuit.layers = [
        #     [0,1,2],
        #     [3,4,None],
        #     [None,5,6],
        #     [7,None,None],
        #     [None,8,None],
        #     [None,9,None],
        #     [None,None,None,None],
        #     [None,10,11,None],
        #     [14,None,None],
        #     [15,None],
        #     [12,13]
        # ]

        canvas = Canvas(root, height=300, width=800, bg="white", highlightthickness=0)
        canvas.pack()
        config = {}
        self.drawing = CircuitDrawing(canvas, circuit, config)

        # self.drawing.drawCircuit()

        root.eval('tk::PlaceWindow . center')
        root.mainloop()

def printtest():
    print("This is a print from /app/window.py")