from .gui import app

if __name__ == "__main__":
    # app.main()

    from .portgraph import PortGraph
    from .cprop import Generator
    from .utils import *

    g = PortGraph()
    H = Generator("H", OBJ1, OBJ1)
    CX = Generator("CX", OBJ11, OBJ11)

