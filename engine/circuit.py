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
    def __init__(self, id, type, dom, cod) -> None:
        """
        Attributs:
            id: int -> id of the node in dag
            type: str -> type of the gate (H, P, CX, D, G, etc.)
            dom: int -> domain (number of input wires)
            cod: int -> codomain (number of output wires)
        """
        self.type = type

    def __str__(self) -> str:
        return ""
    
    def isConnectable(self, gate) -> bool:
        return True

class bound(Gate):
    def __init__(self, id) -> None:
        super().__init__(id, "", 1, 1)

class H(Gate):
    def __init__(self, id) -> None:
        super().__init__(id, "H", 1, 1)

class P(Gate):
    def __init__(self, id, param) -> None:
        self.param = param
        super().__init__(id, "P", 1, 1)

class CNOT(Gate):
    def __init__(self, id) -> None:
        super().__init__(id, "CX", 2, 2)

class Divider(Gate):
    def __init__(self, id, dom, cod) -> None:
        super().__init__(id, "D", dom, cod)

class gatherer(Gate):
    def __init__(self, id, dom, cod) -> None:
        super().__init__(id, "D", dom, cod)


########################### Circuit class ############################
class Circuit:
    """Class of quantum circuits"""

    def __init__(self, name, gates, adj) -> None:
        """
        Attributs:
            name: str -> name of the circuit
            gates: [Gate] -> list of gates indexed by gate id
            adj: ->
        """
        self.name = name

    def __str__(self) -> str:
        return "This circuit is called: " + self.name
    
    def checkConnectivity(self) -> bool:
        return True