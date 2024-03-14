import gui as app
from engine import *

config = {
    "wire-width": 1,
    "box-fill": "white"
}

if __name__ == "__main__":
    print("--- Patoc: a graphical tool for quantum circuits ---")


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
        ["i",5,6],
        [7,"i"],
        ["i",8,"i"],
        ["i",9,"i"],
        ["i","i","i","i"],
        ["i",10,11]
    ]

    app.MainWindow()


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
