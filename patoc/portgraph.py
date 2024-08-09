from __future__ import annotations

from .cprop import Color, Object, Generator, Arrow, Composition
from .utils import *


########################### Port class ############################
class Port:
    """Class of port in portgraphs"""

    def __init__(self, node: Node, id: int, color: Color) -> None:
        self._node: Node = node
        self._graph: PortGraph = node.graph
        self._id: int = id
        self._color: Color = color
        self._dest: Port = None
    
    def __str__(self):
        """str(G)"""
        s = "(" + str(self.color) + ") "
        if self._dest:  s += str(self._dest.node.id)
        else: s += "None"
        return s

    @property
    def node(self) -> Node: return self._node

    @property
    def id(self) -> Node: return self._id

    @property
    def color(self) -> Color: return self._color

    @property
    def dest(self) -> Color: return self._dest

    @dest.setter
    def dest(self, dest_port: Port) -> None:
        assert dest_port.color == self.color
        self._dest = dest_port

    def connect(self, neighbor) -> None: self.dest = neighbor



########################### Node class ############################
class Node:
    """Class of nodes in portgraphs"""

    def __init__(self, graph: PortGraph, id: int, arrow: Arrow) -> None:
        self._graph: PortGraph = graph
        self._id: int = id
        self.arrow: Arrow = arrow
        self.in_ports: list[Port] = [Port(self, i, arrow.domain[i]) for i in range(len(arrow.domain)) if arrow.domain[i] != Color(0)]
        self.out_ports: list[Port] = [Port(self, i, arrow.codomain[i]) for i in range(len(arrow.codomain)) if arrow.codomain[i] != Color(0)]

    def __eq__(self, other: Node) -> bool:
        return other.id == self.id
    
    def __ne__(self, other: Node) -> bool:
        return not self.__eq__(other)

    @property
    def graph(self) -> PortGraph: return self._graph

    @property
    def id(self) -> int: return self._id

    @property
    def domain(self) -> Object: return self.arrow.domain

    @property
    def codomain(self) -> Object: return self.arrow.codomain

    def in_port(self, i) -> Port: return self.inports[i]

    def out_port(self, i) -> Port: return self.outports[i]

    @property
    def in_nodes(self) -> list[Node]:
        return [in_port.dest.node for in_port in self.in_ports]
    
    @property
    def out_nodes(self) -> list[Node]:
        return [out_port.dest.node for out_port in self.out_ports]

    def print(self) -> None:
        print("--- Node id:", self.id, "---")
        if type(self.arrow) == Arrow: print("Arrow:", str(self.arrow.generator))
        elif type(self.arrow) == Composition: print("Arrow:", str(self.arrow.to_term()))
        s_in_ports = ""
        for port in self.in_ports: s_in_ports += "[" + str(port) + "] "
        print("Input Ports:", s_in_ports)
        s_out_ports = ""
        for port in self.out_ports: s_out_ports += "[" + str(port) + "] "
        print("Output Ports:", s_out_ports)

    def relative_depth(self, node: Node) -> int:
        relative_depth = dict()

        # explore iterative successors
        relative_depth[self.id] = 0
        for out_node in self.out_nodes: relative_depth[out_node.id] = 1
        queue = self.out_nodes
        while len(queue)>0:
            current = queue.pop(0)
            current_relative_depth = relative_depth[current.id]
            for out_node in current.out_nodes:
                if out_node.id in relative_depth.keys():
                    relative_depth[out_node.id] = max(current_relative_depth+1, relative_depth[out_node.id])
                else:
                    relative_depth[out_node.id] = current_relative_depth+1
                queue.append(out_node)
        
        if node.id in relative_depth.keys(): return relative_depth[node.id]

        # explore iterative predecessors
        relative_depth[self.id] = 0
        for in_node in self.in_nodes: relative_depth[in_node.id] = -1
        queue = self.in_nodes
        while len(queue)>0:
            current = queue.pop(0)
            current_relative_depth = relative_depth[current.id]
            for in_node in current.in_nodes:
                if in_node.id in relative_depth.keys():
                    relative_depth[in_node.id] = min(current_relative_depth-1, relative_depth[in_node.id])
                else:
                    relative_depth[in_node.id] = current_relative_depth-1
                queue.append(in_node)

        if node.id in relative_depth.keys(): return relative_depth[node.id]
        else: return 0



########################### PortGraph class ############################
class PortGraph:
    """Class of portgraphs"""

    OBJ0 = Object([Color(0)])

    def __init__(self, domain: Object, codomain: Object) -> None:
        self._nodes = []
        self._next_id = 0

        self._inputs = []
        for color in domain:
            obj = Object([color])
            gen = Generator("in", self.OBJ0, obj)
            input = Node(self, self.next_id, Arrow(gen))
            self._inputs.append(input)
        self._nodes += self._inputs

        self._outputs = []
        for color in codomain:
            obj = Object([color])
            gen = Generator("out", obj, self.OBJ0)
            output = Node(self, self.next_id, Arrow(gen))
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
        print("===================================")
        for node in self.nodes:
            node.print()
        print("===================================")

    @property
    def nodes(self) -> list[Node]: return self._nodes

    @property
    def inputs(self) -> list[Node]: return self._inputs

    @property
    def outputs(self) -> list[Node]: return self._outputs

    def input(self, i) -> Node: return self._inputs[i]

    def output(self, i) -> Node: return self._outputs[i]

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

    @property
    def next_id(self) -> int:
        self._next_id += 1
        return self._next_id-1

    def add_node(self, generator: Generator) -> Node:
        arrow = Arrow(generator)
        node = Node(self, self.next_id, arrow)
        self._nodes.append(node)
        return node

    def push_node(self, node: Node) -> None:
        self._nodes.append(node)
        return node

    def remove_node(self, node: Node) -> None:
        assert node in self._nodes
        self._nodes.remove(node)

    def add_edge_from_ports(self, from_port: Port, to_port: Port) -> None:
        from_port.connect(to_port)
        to_port.connect(from_port)
    
    def add_edge_from_nodes(self, from_node: tuple[Node, int], to_node: tuple[Node, int]) -> None:
        from_port = from_node[0].out_ports[from_node[1]]
        to_port = to_node[0].in_ports[to_node[1]]
        self.add_edge_from_ports(from_port, to_port)

    def has_edge(self, from_node: Node, to_node: Node) -> bool:
        return False
    
    def relative_depth(self, from_node: Node, to_node: Node) -> int:
        return from_node.relative_depth(to_node)

    def merge_nodes(self, node1: Node, node2: Node) -> None:
        relative_depth = self.relative_depth(node1, node2)
        assert abs(relative_depth)<=1 # nodes are not directly mergable

        # nodes are parallel and can be merged using tensor
        if relative_depth == 0:
            arrow = Composition("*", node1.arrow, node2.arrow)
            merge = Node(self, self.next_id, arrow)
            self.push_node(merge)

            # connect input ports
            in_ports_dest1 = [port.dest for port in node1.in_ports]
            in_ports_dest2 = [port.dest for port in node2.in_ports]
            in_ports_dest = in_ports_dest1 + in_ports_dest2
            for i in range(len(in_ports_dest)):
                in_port_dest = in_ports_dest[i]
                in_port = merge.in_ports[i]
                self.add_edge_from_ports(in_port_dest, in_port)

            # connect output ports
            out_ports_dest1 = [port.dest for port in node1.out_ports]
            out_ports_dest2 = [port.dest for port in node2.out_ports]
            out_ports_dest = out_ports_dest1 + out_ports_dest2
            for i in range(len(out_ports_dest)):
                out_port_dest = out_ports_dest[i]
                out_port = merge.out_ports[i]
                self.add_edge_from_ports(out_port_dest, out_port)
        
        # nodes are adjacent and can be merged using sequencial compostion
        else:
            left,right = node1,node2
            if relative_depth < 0: left,right = node2,node1

            domain = left.domain
            codomain = right.codomain
            in_ports = left.in_ports
            out_ports = left.out_ports

            perm = dict()

            for out_port in left.out_ports:
                if out_port.dest.node == right:
                    perm[out_port.id] = out_port.dest.id
                else:
                    codomain.append(out_port.color)
                    perm[out_port.id] = len(out_ports)
                    out_ports.append(out_port)
                
            for in_port in right.in_ports:
                if in_port.dest.node != left:
                    domain.append(in_port.color)
                    perm[len(in_ports)] = in_port.id
                    in_ports.append(in_port)
                    
            print(domain)
            print(perm)
            print(codomain)

        
        self.remove_node(node1)
        self.remove_node(node2)
        
    def split_node(self, node: Node, composition: Composition) -> None:
        pass
        