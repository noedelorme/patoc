# import gui as app
# from gui.tk_window import App as TkApp
from gui.app import Patoc
from engine.circuit import Circuit
from engine.grid import Grid

if __name__ == "__main__":
    print("--- Patoc: a graphical tool for quantum circuits ---")

    app = Patoc()
    app.exec()

    # from data.examples import circuit1, subcircuit1, czLHS

    # print("The big circuit is ")
    # circuit1.print()
    # print("------------------------------")
    # print("The small circuit is ")
    # subcircuit1.print()
    # print("------------------------------")
    # circuit1.matchAxiom(subcircuit1)
    # print("------------------------------")



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