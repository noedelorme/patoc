# import gui as app
from gui.tk_window import App as TkApp
from gui.app import Patoc
from engine.circuit import Circuit
from engine.grid import Grid

config = {
    "wire-width": 1,
    "box-fill": "white"
}

if __name__ == "__main__":
    print("--- Patoc: a graphical tool for quantum circuits ---")

    app = Patoc()
    app.exec()




    # app = TkApp()
    # app.mainloop()


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


    # # test circuit containing LHS of axiom CZ
    # circuit2 = Circuit("My circuit")
    # org1 = circuit2.gate("in", org=True)
    # org2 = circuit2.gate("in", org=True)
    # org3 = circuit2.gate("in", org=True)
    # org4 = circuit2.gate("in", org=True)
    # h1 = circuit2.gate("H")
    # a = circuit2.gate("A", dom=2)
    # h2 = circuit2.gate("H")
    # p = circuit2.gate("P", dom=3)
    # h3 = circuit2.gate("H")
    # b = circuit2.gate("B", dom=2)
    # u = circuit2.gate("U", dom=2)
    # dst1 = circuit2.gate("out", dst=True)
    # dst2 = circuit2.gate("out", dst=True)
    # dst3 = circuit2.gate("out", dst=True)
    # dst4 = circuit2.gate("out", dst=True)
    # h4 = circuit2.gate("H")
    # circuit2.connect(org1, b, wiring=(0,0))
    # circuit2.connect(org2, h1, wiring=(0,0))
    # circuit2.connect(org3, a, wiring=(0,0))
    # circuit2.connect(org4, a, wiring=(0,1))
    # circuit2.connect(a, h2, wiring=(0,0))
    # circuit2.connect(a, p, wiring=(1,2))
    # circuit2.connect(h1, p, wiring=(0,0))
    # circuit2.connect(h2, p, wiring=(0,1))
    # circuit2.connect(p, b, wiring=(0,1))
    # circuit2.connect(p, h3, wiring=(1,0))
    # circuit2.connect(b, dst1, wiring=(0,0))
    # circuit2.connect(b, u, wiring=(1,0))
    # circuit2.connect(h3, u, wiring=(0,1))
    # circuit2.connect(u, dst2, wiring=(0,0))
    # circuit2.connect(u, h4, wiring=(1,0))
    # circuit2.connect(h4, dst3, wiring=(0,0))
    # circuit2.connect(p, dst4, wiring=(2,0))

    # grid = Grid(circuit2)

    # for gate in circuit2.gates:
    #     print(gate.type, gate.id)