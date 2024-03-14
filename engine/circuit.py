########################### Parameter class ##########################
class Parameter:
    def __init__(self, symbolic, value) -> None:
        """
        Attributs:
            symbolic: bool -> type of the parameter (False for value, True for symbol)
            value: str -> mathematical description
        """
        self.symbolic = symbolic
        self.value = value


############################# Gate class #############################
class Gate:
    def __init__(self, id, type, dom, cod, preset, postset) -> None:
        """
        Attributs:
            id: int -> id of the node in dag
            type: str -> type of the gate (H, P, CX, D, G, etc.)
            dom: int -> domain (number of input wires)
            cod: int -> codomain (number of output wires)
            preset: [int] -> list of predecessors ids
            postset: [int] -> list of successors ids
        """
        self.id = id
        self.type = type
        self.dom = dom
        self.cod = cod
        self.preset = preset
        self.postset = postset
        self.depth = 0

    def __str__(self) -> str:
        return str(self.preset)+" <<< "+str(self.type)+"("+str(self.id)+") >>> " + str(self.postset)
    
    def isConnectable(self, gate) -> bool:
        return True   

class bound(Gate):
    def __init__(self, id, preset, postset) -> None:
        super().__init__(id, "", 1, 1, preset, postset)

class H(Gate):
    def __init__(self, id, preset, postset) -> None:
        super().__init__(id, "H", 1, 1, preset, postset)

class P(Gate):
    def __init__(self, id, param, preset, postset) -> None:
        self.param = param
        super().__init__(id, "P", 1, 1, preset, postset)

class SWAP(Gate):
    def __init__(self, id, preset, postset) -> None:
        super().__init__(id, "SWAP", 2, 2, preset, postset)

class CNOT(Gate):
    def __init__(self, id, preset, postset) -> None:
        super().__init__(id, "CX", 2, 2, preset, postset)

class Divider(Gate):
    def __init__(self, id, preset, postset) -> None:
        super().__init__(id, "D", 1, 2, preset, postset)

class Gatherer(Gate):
    def __init__(self, id, preset, postset) -> None:
        super().__init__(id, "G", 2, 1, preset, postset)


########################### Circuit class ############################
class Circuit:
    """Class of quantum circuits"""

    def __init__(self, name, gates, org, dst) -> None:
        """
        Attributs:
            name: str -> name of the circuit
            gates: [Gate] -> list of gates indexed by gate id
            org: [int] -> list of origin nodes ids
            dst: [int] -> list of destination nodes ids
        """
        self.name = name
        self.gates = gates
        self.org = org
        self.dst = dst
        self.dom = len(org)
        self.cod = len(dst)

        self.layers = []

    def __str__(self) -> str:
        return "This circuit is called: " + self.name

    def connect(self, idorg, iddst, wiring) -> None:
        self.gates[idorg].postset.append((wiring,iddst))
        self.gates[iddst].preset.append((wiring,idorg))
    
    def checkConnectivity(self) -> bool:
        return True
    
    # highly inefficient, should be dynamic programing
    def updateDepth(self) -> None:
        queue = self.org
        while len(queue)>0:
            currentgate = self.gates[queue.pop(0)]
            maxpredepth = -1
            for (qubit,pre) in currentgate.preset:
                maxpredepth = max(maxpredepth, self.gates[pre].depth)
            currentgate.depth = maxpredepth+1
            for (qubit,post) in currentgate.postset:
                queue.append(post)
            