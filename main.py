import gui as app
from engine import *

config = {
    "wire-width": 1,
    "box-fill": "white"
}

if __name__ == "__main__":
    print("--- Patoc: a graphical tool for quantum circuits ---")

    window = app.MainWindow()

    # import tkinter as tk
    # class Main(tk.Tk):
    #     def __init__(self): 
    #         super().__init__()
    #         self.canvas = tk.Canvas(self, width=500, height=300)
    #         self.canvas.grid(row=0,column=0)
    #         self._cLabel = tk.Label(self.canvas, text='Hello World', bg='blue')
    #         self.id_cLabel = self.canvas.create_window(100,100, window=self._cLabel,    tags="motion_bound")
    #         self.update()
    #         self._cLabel.bind("<B1-Motion>", self.relocate)

    #     def relocate(self, event):
    #         print(self.canvas.winfo_pointerxy())
    #         x0,y0 = self.canvas.winfo_pointerxy()
    #         x0 -= self.canvas.winfo_rootx()
    #         y0 -= self.canvas.winfo_rooty()
    #         self.canvas.coords(self.id_cLabel,x0,100)

    # main = Main()
    # main.mainloop()



    # from openqasm3 import parser
    # from openqasm3.ast import QuantumGate
    # from openqasm3.ast import QubitDeclaration

    # q = 'OPENQASM 3.0;include "stdgates.inc";qubit[2] q;h q[1];cx q[0], q[1];h q[1];'
    # p = "OPENQASM 3.0;qubit[2] q;"

    # s = parser.parse(q).statements

    # for x in s:
    #     print("----------------------------")
    #     print(x)
    #     print(type(x)==QuantumGate)

    # org1 = bound(0, [], [])
    # org2 = bound(1, [], [])
    # h1 = H(2, [], [])
    # cx = CNOT(3, [], [])
    # h2 = H(4, [], [])
    # dst1 = bound(5, [], [])
    # dst2 = bound(6, [], [])
    # circuit = Circuit("cz-one-cnot", [org1,org2,h1,cx,h2,dst1,dst2],[0,1],[5,6])
    # circuit.connect(0, 3, qubit=1)
    # circuit.connect(1, 2, qubit=2)
    # circuit.connect(2, 3, qubit=2)
    # circuit.connect(3, 5, qubit=1)
    # circuit.connect(3, 4, qubit=2)
    # circuit.connect(4, 6, qubit=2)

    # print("===================================")
    # circuit.updateDepth()
    # for gate in circuit.gates:
    #     print(gate)
    #     print(gate.depth)








    # from tkinter import *
    # import networkx as nx
    # import matplotlib.pyplot as plt
    # from matplotlib.figure import Figure
    # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # root = Tk()

    # f = Figure(figsize=(5,2))
    # a = f.add_subplot(111)

    # G = nx.Graph()
    # G.add_edges_from([(1 ,2) , (2 ,3) , (1 ,3) , (1 ,4) ])
    # nx.draw(G, ax=a)

    # dagcanvas = FigureCanvasTkAgg(f, root)
    # dagcanvas.get_tk_widget().pack()


    # root.mainloop()