import gui as app
from engine import *

config = {
    "wire-width": 1,
    "box-fill": "white"
}

if __name__ == "__main__":
    print("--- Patoc: a graphical tool for quantum circuits ---")

    window = app.MainWindow()



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