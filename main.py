# import gui as app
from gui.window import App
from engine import *

config = {
    "wire-width": 1,
    "box-fill": "white"
}

if __name__ == "__main__":
    print("--- Patoc: a graphical tool for quantum circuits ---")

    app = App()
    app.mainloop()




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