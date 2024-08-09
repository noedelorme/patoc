from __future__ import annotations
from typing import Iterable

from .binarytree import BinaryTree


########################### Color class ############################
class Color:
    """Class of colors in a colored prop"""

    def __init__(self, value: str|int) -> None:
        self._value = value
    
    def __str__(self) -> str:
        """str(self)"""
        return str(self.value)

    def __eq__(self, other: Color):
        """self == other"""
        return other.value == self.value
    
    def __ne__(self, other: Color):
        """self != other"""
        return not self.__eq__(other)

    @property
    def value(self) -> str|int:
        if type(self._value) == int: return self._value
        elif self._value.isnumeric(): return int(self._value)
        else: return self._value
    
    def is_numeric(self) -> bool:
        return self.value.isnumeric()


########################### Object class ############################
class Object:
    """Class of objects in a colored prop"""

    def __init__(self, _colors: list[Color]) -> None:
        self._colors = _colors
    
    def __str__(self) -> str:
        """str(self)"""
        s = str(self.colors[0])
        for i in range(1,len(self.colors)):
            c = str(self.colors[i])
            s += " * " + c
        return s

    def __len__(self) -> int:
        """len(self)"""
        return len(self.colors)

    def __getitem__(self, i) -> Color:
        """self[i]"""
        return self.colors[i]

    def __iter__(self) -> Iterable[Color]:
        """for x in self"""
        return self.colors.__iter__()

    def __eq__(self, other: Object) -> bool:
        """self == other"""
        if len(other) != len(self): return False
        for i in range (len(other)):
            if other[i] != self[i]: return False
        return True

    def __ne__(self, other: Object) -> bool:
        """self != other"""
        return not self.__eq__(other)
    
    @property
    def colors(self) -> list[Color]:
        return self._colors
    
    def append(self, color: Color) -> None:
        self._colors.append(color)
    
    def tensor(self, other: Object) -> Object:
        return Object(self.colors + other.colors)
    

########################### Generator class ############################
class Generator:
    """Class of generators in a colored prop"""

    def __init__(self, name: str, domain: Object, codomain: Object) -> None:
        self._name = name
        self._domain = domain
        self._codomain = codomain

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Generator) -> bool:
        """self == other"""
        return other.name == self.name and other.domain == self.domain and other.codomain == self.codomain

    def __ne__(self, other: Generator) -> bool:
        """self != other"""
        return not self.__eq__(other)

    @property
    def name(self) -> Object:
        return self._name
    
    @property
    def domain(self) -> Object:
        return self._domain
    
    @property
    def codomain(self) -> Object:
        return self._codomain


########################### Abstract arrow class ############################
class AbstractArrow:
    """Abstract class of arrows (or morphisms) in a colored prop"""

    def __init__(self) -> None:
        self.domain: Object = None
        self.codomain: Object = None

    def compose(self, other: Arrow, reverse: bool = False) -> Arrow:
        left,right = self,other
        if reverse: left,right = other,self

        assert left.codomain == right.domain
        result = Composition(";", left, right)
        return result

    def compose(self, other: Arrow, reverse: bool = False) -> Arrow:
        top,bottom = self,other
        if reverse: top,bottom = other,self
        result = Composition("*", top, bottom)
        return result


########################### Arrow class ############################
class Arrow(AbstractArrow):
    """Class of basic arrows in a colored prop"""

    def __init__(self, generator: Generator) -> None:
        super().__init__()

        self._generator: Generator = generator
        self.domain = generator.domain
        self.codomain = generator.codomain
    
    @property
    def generator(self) -> Object: return self._generator
    
    def print(self) -> None:
        print(self.generator)


########################### Arrow class ############################
class Composition(AbstractArrow):
    """Class of compositional arrows in a colored prop"""

    def __init__(self, symbol: str, left: Arrow, right: Arrow) -> None:
        super().__init__()

        self._symbol: str = symbol
        self._left: Arrow = left
        self._right: Arrow= right

        if symbol == ";":
            self.domain = left.domain
            self.codomain = right.codomain
        elif symbol == "*":
            self.domain = left.domain.tensor(right.domain)
            self.codomain = left.codomain.tensor(right.codomain)
    
    @property
    def symbol(self) -> Object: return self._symbol

    @property
    def left(self) -> Object: return self._left

    @property
    def right(self) -> Object: return self._right
    
    def print(self) -> None:
        print(self.symbol)
        self.left.print()
        self.right.print()

    def to_term(self) -> str:
        return "no yet implemented"