from __future__ import annotations

from .cprop import Color, Object, Generator, Arrow
from .utils import *


########################### Port class ############################
class Port:
    """Class of port in portgraphs"""

    def __init__(self, node: Node, color: Object) -> None:
        self._node: Node = node
        self._color: Object = color
        self.dest: Port = None

    @property
    def node(self) -> Node: return self._node

    @property
    def color(self) -> Object: return self._color

    def connect(self, neighbor) -> None: self.dest = neighbor



########################### Node class ############################
class Node:
    """Class of nodes in portgraphs"""

    def __init__(self, graph: PortGraph, id: int, arrow: Arrow) -> None:
        self._graph: PortGraph = graph
        self._id: int = id
        self.arrow: Arrow = arrow
        self.inport: list[Port] = [Port(self, color) for color in arrow.domain]
        self.outport: list[Port] = [Port(self, color) for color in arrow.codomain]

    @property
    def graph(self) -> PortGraph: return self._graph

    @property
    def id(self) -> int: return self._id

    @property
    def domain(self) -> Arrow: return self.arrow.domain

    @property
    def codomain(self) -> Arrow: return self.arrow.codomain



########################### PortGraph class ############################
class PortGraph:
    """Class of portgraphs"""

    OBJ0 = Object([Color(0)])

    def __init__(self, domain: Object, codomain: Object) -> None:
        self._nodes = []

        self._inputs = []
        for color in domain:
            obj = Object([color])
            gen = Generator("in", self.OBJ0, obj)
            input = Node(self, len(self._inputs), Arrow(gen))
            self._inputs.append(input)
        self._nodes += self._inputs

        self._outputs = []
        for color in codomain:
            obj = Object([color])
            gen = Generator("out", obj, self.OBJ0)
            output = Node(self, len(self._outputs), Arrow(gen))
            self._outputs.append(output)
        self._nodes += self._outputs
    
    def __str__(self):
        """str(G)"""
        pass

    def __len__(self):
        """len(G)"""
        pass

    def __getitem__(self, n):
        """G[n]"""
        pass

    def __iter__(self):
        """for n in G"""
        pass
    
    def __contains__(self, n):
        """n in G"""
        return True
    
    def print(self) -> None:
        pass

    @property
    def nodes(self) -> list[Node]: return self._nodes

    @property
    def input(self) -> list[Node]: return self._inputs

    @property
    def output(self) -> list[Node]: return self._outputs

    @property
    def domain(self) -> int:
        return len(self._inputs) # utiliser tensor of object in utils
    
    @property
    def codomain(self) -> int:
        return len(self._outputs) # utiliser tensor of object in utils
    
    @property
    def number_of_nodes(self) -> int: return len(self.nodes)
    
    @property
    def number_of_edges(self) -> int:
        pass
    
    @property
    def depth(self) -> int:
        pass

    def add_node(self, generator: Generator) -> None:
        id = self.number_of_nodes
        arrow = Arrow(generator)
        self._nodes.append(Node(self, id, arrow))

    def remove_node(self) -> None:
        pass

    def add_edge(self, node1, port1, ) -> None:
        pass

    def has_edge(self) -> bool:
        pass