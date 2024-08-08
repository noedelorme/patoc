from .gui import app

if __name__ == "__main__":
    # app.main()

    from .portgraph import PortGraph
    from .cprop import Color, Object, Generator, Arrow, Composition
    from .utils import *

    COL0 = Color("0")
    COL1 = Color("1")
    COLn = Color("n")
    COLm = Color("m")

    OBJ0 = Object([COL0])
    OBJ1 = Object([COL1])
    OBJ11 = Object([COL1,COL1])

    e = Generator("e", OBJ0, OBJ0)
    id = Generator("id(1)", OBJ1, OBJ1)
    h = Generator("H", OBJ1, OBJ1)
    cx = Generator("CX", OBJ11, OBJ11)

    div = Generator("div", Object([Color("n+1")]), Object([Color("n"),Color("1")]))

    a = Arrow(id)
    b = Arrow(h)
    c = Arrow(h)
    d = Arrow(cx)
    f = Arrow(id)
    i = Arrow(id)

    g = Composition(";", a, b)
    j = Composition("*", g, i)
    h = Composition("*", c, f)
    k = Composition(";", j, h)
    l = Composition(";", k, d)

    l.print()
    print(l.domain, l.codomain)



