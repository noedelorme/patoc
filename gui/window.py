from tkinter import * 
from gui.painter import CircuitPainter
from engine import *

class MainWindow:
    def __init__(self) -> None:
        root = Tk()
        root.title("Patoc: a graphical tool for quantum circuits")
        # label = Label(root, text="Hello World")
        # label.pack()

        org1 = bound(0, [], [])
        org2 = bound(1, [], [])
        org3 = bound(2, [], [])
        h1 = H(3, [], [])
        cx1 = CNOT(4, [], [])
        h2 = H(5, [], [])
        p1 = P(6, "0", [], [])
        cx2 = CNOT(7, [], [])
        h3 = H(8, [], [])
        d1 = Divider(9, [], [])
        h4 = H(10, [], [])
        cx3 = CNOT(11, [], [])
        dst1 = bound(12, [], [])
        dst2 = bound(13, [], [])
        dst3 = bound(14, [], [])
        dst4 = bound(15, [], [])
        circuit = Circuit("cz-one-cnot", [org1,org2,org3,h1,cx1,h2,p1,cx2,h3,d1,h4,cx3,dst1,dst2,dst3,dst4],[0,1,2],[12,13,14,15])
        circuit.connect(0, 3, wiring=(1,1))
        circuit.connect(1, 4, wiring=(1,1))
        circuit.connect(2, 4, wiring=(1,2))
        circuit.connect(3, 7, wiring=(1,1))
        circuit.connect(4, 5, wiring=(1,1))
        circuit.connect(4, 6, wiring=(2,1))
        circuit.connect(5, 7, wiring=(1,2))
        circuit.connect(6, 11, wiring=(1,2))
        circuit.connect(7, 12, wiring=(1,1))
        circuit.connect(7, 8, wiring=(2,1))
        circuit.connect(8, 9, wiring=(1,1))
        circuit.connect(9, 10, wiring=(1,1))
        circuit.connect(9, 11, wiring=(2,1))
        circuit.connect(10, 13, wiring=(1,1))
        circuit.connect(11, 14, wiring=(1,1))
        circuit.connect(11, 15, wiring=(1,2))

        circuit.layers = [
            [3,4],
            [None,5,6],
            [7,None],
            [None,8,None],
            [None,9,None],
            [None,None,None,None],
            [None,10,11]
        ]

        canvas = Canvas(root, height=200, width=400)
        canvas.pack()
        config = {}
        self.painter = CircuitPainter(canvas, circuit, config)

        self.painter.drawCircuit()

        root.eval('tk::PlaceWindow . center')
        root.mainloop()

def printtest():
    print("This is a print from /app/window.py")