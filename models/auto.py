from typing import Optional, Dict, List, Set


class Vertex:
    terminal: bool
    delta: Dict[str, Set['Vertex']]
    index: int

    def __init__(self, terminal: bool, delta: Dict[str, Set['Vertex']], index: int = -1):
        self.terminal = terminal
        self.delta = delta
        self.index = index

    def __eq__(self, other):
        if isinstance(other, Vertex):
            if self.index < 0 or other.index < 0:
                return self.__repr__() == other.__repr__()
            return self.index == other.index
        return False

    def __hash__(self):
        if self.index < 0:
            return hash(self.__repr__())
        return hash(self.index)


class Automaton:
    start: Vertex
    vertices: Set[Vertex]

    def __init__(self, start: Vertex, vertices: Set[Vertex]):
        self.start = start
        self.vertices = vertices
