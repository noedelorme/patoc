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
    def __init__(self, id, type, arity=1, pos=(None,None)) -> None:
        """
        Attributs:
            id: int -> id of the node in dag
            type: str -> type of the gate (H, P, CX, D, G, etc.)
            arity: int -> domain
            preset: [int] -> list of predecessors ids
            postset: [int] -> list of successors ids
        """
        self.id = id
        self.type = type
        self.arity = arity
        self.preset = []
        self.postset = []
        self.pos = pos
        self.depth = 0 # to compute for patern matching condition

        if type == "CNOT": self.arity = 2

    def __str__(self) -> str:
        return str(self.preset)+" <<< "+str(self.type)+"("+str(self.id)+") >>> " + str(self.postset)
    
    def isConnectable(self, gate) -> bool:
        return True
    
    def addPredecessor(self, id, wiring) -> None:
        self.preset.append((id,wiring))

    def addSuccessor(self, id, wiring) -> None:
        self.postset.append((id,wiring))

# class Bound(Gate):
#     def __init__(self, id, preset=[], postset=[], pos=(None,None)) -> None:
#         super().__init__(id, "", 1, 1, preset, postset, pos)

# class H(Gate):
#     def __init__(self, id, preset=[], postset=[], pos=(None,None)) -> None:
#         super().__init__(id, "H", 1, 1, preset, postset, pos)

# class P(Gate):
#     def __init__(self, id, param, preset=[], postset=[], pos=(None,None)) -> None:
#         self.param = param
#         super().__init__(id, "P", 1, 1, preset, postset, pos)

# class SWAP(Gate):
#     def __init__(self, id, preset=[], postset=[], pos=(None,None)) -> None:
#         super().__init__(id, "SWAP", 2, 2, preset, postset, pos)

# class CNOT(Gate):
#     def __init__(self, id, preset=[], postset=[], pos=(None,None)) -> None:
#         super().__init__(id, "CX", 2, 2, preset, postset, pos)

# class Divider(Gate):
#     def __init__(self, id, preset=[], postset=[], pos=(None,None)) -> None:
#         super().__init__(id, "D", 1, 2, preset, postset, pos)

# class Gatherer(Gate):
#     def __init__(self, id, preset=[], postset=[], pos=(None,None)) -> None:
#         super().__init__(id, "G", 2, 1, preset, postset, pos)


########################### Circuit class ############################
class Circuit:
    """Class of quantum circuits"""

    def __init__(self, name, gates, org) -> None:
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
        self.dom = len(org)

    def __str__(self) -> str:
        return "This circuit is called: " + self.name

    def connect(self, org, dst, wiring) -> None:
        org.addSuccessor(dst.id,wiring)
        dst.addPredecessor(org.id,wiring)
    
    def checkConnectivity(self) -> bool:
        return True
    
    # highly inefficient, should be dynamic programing
    def updateDepth(self) -> None:
        queue = self.org.copy()
        while len(queue)>0:
            currentgate = self.gates[queue.pop(0)]
            maxpredepth = -1
            for (qubit,pre) in currentgate.preset:
                maxpredepth = max(maxpredepth, self.gates[pre].depth)
            currentgate.depth = maxpredepth+1
            for (qubit,post) in currentgate.postset:
                queue.append(post)
            