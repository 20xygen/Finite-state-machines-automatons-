from models.auto import Automaton, Vertex
from typing import Dict, Set, Optional
from operations.transform import sign


class BidirectionalVertex(Vertex):
    reverse: Dict[str, Set['Vertex']]

    def __init__(self, terminal: bool, delta: Dict[str, Set['Vertex']],
                 reverse: Dict[str, Set['Vertex']], index: int = -1):
        super().__init__(terminal, delta, index)
        self.reverse = reverse


class BidirectionalAutomaton:  # no inheritance in case of BidirectionalVertice variables' type
    start: BidirectionalVertex
    vertices: Set[BidirectionalVertex]
    end: Optional[BidirectionalVertex]

    def __init__(self, auto: Automaton, single_end: bool = False):
        sign(auto)
        vert_list = [BidirectionalVertex(False, {}, {}, i) for i in range(len(auto.vertices))]
        self.start = vert_list[0]  # assume that given automaton's start's index is also 0
        for vert in auto.vertices:
            for sym, tos in vert.delta.items():
                for to in tos:
                    new_vert = vert_list[vert.index]
                    new_to = vert_list[to.index]
                    if sym not in new_vert.delta.keys():
                        new_vert.delta[sym] = set()
                    if sym not in new_to.reverse.keys():
                        new_to.reverse[sym] = set()
                    new_vert.delta[sym].add(new_to)
                    new_to.reverse[sym].add(new_vert)
        if single_end:
            self.end = BidirectionalVertex(True, {}, {'': set()}, len(vert_list))
            vert_list.append(self.end)
            for vert in auto.vertices:
                new_vert = vert_list[vert.index]
                new_vert.terminal = vert.terminal
                if vert.terminal:
                    new_vert.terminal = False
                    if '' not in new_vert.delta.keys():
                        new_vert.delta[''] = set()
                    new_vert.delta[''].add(self.end)
                    self.end.reverse[''].add(new_vert)
        else:
            self.end = None
        self.vertices = set(vert_list)