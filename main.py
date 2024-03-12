import gui as app
from engine import *

config = {
    "wire-width": 1,
    "box-fill": "white"
}

if __name__ == "__main__":
    print("--- Patoc: a graphical tool for quantum circuits ---")

    # app.MainWindow()

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
