from __future__ import annotations

from .cprop import Color, Object, Arrow
from .utils import *

########################### PortGraph class ############################
class Node:
    """Class of nodes in portgraphs"""

    def __init__(self, graph: PortGraph, id: int, arrow: Arrow) -> None:
        self._graph = graph
        self._id = id

    @property
    def graph(self) -> PortGraph:
        return self._graph

    @property
    def id(self) -> int:
        return self._id


########################### PortGraph class ############################
class PortGraph:
    """Class of portgraphs"""

    def __init__(self) -> None:
        self._nodes = []
        self._input = []
        self._output = []
    
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
    def nodes(self) -> list[Node]:
        return self._nodes

    @property
    def domain(self) -> int:
        return len(self._input) # utiliser tensor of object in utils
    
    @property
    def codomain(self) -> int:
        return len(self._output)
    
    @property
    def number_of_nodes(self) -> int:
        return len(self._nodes)
    
    @property
    def number_of_edges(self) -> int:
        return 0
    
    @property
    def depth(self) -> int:
        pass

    def add_node(self) -> None:
        pass

    def remove_node(self) -> None:
        pass

    def add_edge(self) -> None:
        pass

    def has_edge(self) -> None:
        pass

    def neighbors(self, node) -> None:
        pass