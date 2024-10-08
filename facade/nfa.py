from models.auto import Automaton, Vertex
from typing import Optional, Union
from interface.text import str_to_nfa, nfa_to_str
from pathlib import Path
from operations.poland import to_polish_notation, polska_into_auto
from operations.transform import determinate, minimize, make_complete, complement, eps_closure
from operations.regexify import to_regex
from interface.graph import visualize_automaton
from typing import Set


class NFA:
    auto: Optional[Automaton] = None

    def __init__(self, text: Optional[str] = None):
        if text is not None:
            self.auto = str_to_nfa(text)

    def __process_eps(self, pos: int, remaining: str, cur: Vertex) -> bool:  # deprecated
        if '' not in cur.delta.keys():
            return False
        closure: Set[Vertex] = set()
        eps_closure(cur, closure)
        if pos == len(remaining):
            return any([vert.terminal for vert in closure])
        return any([self.__process(pos, remaining, vert) for vert in closure])

    def __process(self, pos: int, remaining: str, cur: Vertex) -> bool:
        closure: Set[Vertex] = set()
        eps_closure(cur, closure)
        if pos == len(remaining):
            return any([vert.terminal for vert in closure])
        sym = remaining[pos]
        for vert in closure:
            if sym in vert.delta.keys():
                for to in vert.delta[sym]:
                    if self.__process(pos + 1, remaining, to):
                        return True
        return False

    def process(self, word: str):
        return self.__process(0, word, self.auto.start)

    def print(self):
        print(nfa_to_str(self.auto))

    def save(self, path: Union[str, Path]):
        with open(path, 'w') as f:
            f.write(nfa_to_str(self.auto))

    @staticmethod
    def by_regex(text: str) -> 'NFA':
        polska = to_polish_notation(text)
        nfa = NFA()
        nfa.auto = polska_into_auto(polska)
        return nfa

    def regex(self) -> str:
        return to_regex(self.auto)

    def visualize(self):
        visualize_automaton(self.auto, 'NFA', True)
