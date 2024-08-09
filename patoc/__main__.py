from .gui import app

if __name__ == "__main__":
    # app.main()

    from .portgraph import PortGraph
    from .cprop import Color, Object, Generator, Arrow, Composition
    from .utils import *

    COL0 = Color(0)
    COL1 = Color(1)
    COL2 = Color(2)
    COLn = Color("n")
    COLm = Color("m")

    OBJ0 = Object([COL0])
    OBJ1 = Object([COL1])
    OBJ2 = Object([COL2])
    OBJ11 = Object([COL1,COL1])
    OBJ21 = Object([COL2,COL1])
    OBJ211 = Object([COL2,COL1,COL1])

    e = Generator("e", OBJ0, OBJ0)
    id = Generator("id(1)", OBJ1, OBJ1)
    h = Generator("h", OBJ1, OBJ1)
    cx = Generator("cx", OBJ11, OBJ11)
    div = Generator("div", Object([Color("n+1")]), Object([Color("n"),Color("1")]))
    gat = Generator("div", Object([Color("n"),Color("1")]), Object([Color("n+1")]))

    two_id = Generator("id(1)", OBJ2, OBJ2)
    two_h = Generator("h", OBJ2, OBJ2)
    two_cx = Generator("cx", OBJ21, OBJ21)

    g = PortGraph(OBJ21, OBJ21)
    id1 = g.add_node(two_id)
    h1 = g.add_node(h)
    cx1 = g.add_node(two_cx)
    h2 = g.add_node(two_id)
    id2 = g.add_node(two_id)

    g.add_edge_from_nodes((g.input(0),0), (id1,0))
    g.add_edge_from_nodes((g.input(1),0), (h1,0))
    g.add_edge_from_nodes((id1,0), (cx1,0))
    g.add_edge_from_nodes((h1,0), (cx1,1))
    g.add_edge_from_nodes((cx1,0), (h2,0))
    g.add_edge_from_nodes((cx1,1), (g.output(1),0))
    g.add_edge_from_nodes((h2,0), (id2,0))
    g.add_edge_from_nodes((id2,0), (g.output(0),0))

    g.print()

    # g.merge_nodes(id1, h1)
    g.merge_nodes(h1, cx1)

    g.print()