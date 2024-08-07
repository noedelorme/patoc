

########################### Color class ############################
class Color:
    """Class of colors in a colored prop"""

    def __init__(self, symbol) -> None:
        self._symbol = symbol
    
    def __str__(self) -> str:
        return self.symbol

    def __eq__(self, other):
        pass

    @property
    def symbol(self) -> str:
        return self._symbol
    
    @property
    def is_numeric(self) -> bool:
        return self.symbol.isnumeric()


########################### Object class ############################
class Object:
    """Class of objects in a colored prop"""

    def __init__(self, _colors: list[Color]) -> None:
        self._colors = _colors
    
    def __str__(self) -> str:
        s = str(self.colors[0])
        for i in range(1,len(self.colors)):
            c = str(self.colors[i])
            s += " * " + c
        return s

    def __eq__(self, other):
        pass
    
    @property
    def colors(self) -> list[Color]:
        return self._colors
    

########################### Generator class ############################
class Generator:
    """Class of generators in a colored prop"""

    def __init__(self, name: str, domain: Object, codomain: Object) -> None:
        self._name = name
        self._domain = domain
        self._codomain = codomain

    def __eq__(self, other):
        pass

    @property
    def name(self) -> Object:
        return self._name
    
    @property
    def domain(self) -> Object:
        return self._domain
    
    @property
    def codomain(self) -> Object:
        return self._codomain


########################### Arrow class ############################
class Arrow:
    """Class of arrows (or morphisms) in a colored prop"""