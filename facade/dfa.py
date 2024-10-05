from models.auto import Automaton, Vertex
from typing import Optional, Union
from interface.text import str_to_dfa, dfa_to_str
from pathlib import Path
from operations.poland import to_polish_notation, polska_into_auto
from operations.transform import determinate, minimize, make_complete, complement
from operations.regexify import to_regex
from facade.nfa import NFA
from interface.graph import visualize_automaton
from interface.tables import print_determinization, print_minimization


class DFA(NFA):
    def __init__(self, text: Optional[str] = None):
        super().__init__()
        if text is not None:
            self.auto = str_to_dfa(text)

    def process(self, word: str) -> bool:
        return super().process(word)

    def print(self):
        print(dfa_to_str(self.auto))

    def save(self, path: Union[str, Path]):
        with open(path, 'w') as f:
            f.write(dfa_to_str(self.auto))

    @staticmethod
    def by_regex(text: str) -> 'DFA':
        polska = to_polish_notation(text)
        auto = polska_into_auto(polska)
        dfa = DFA()
        sigma = set()
        for sym in text:
            if sym not in ['_', '+', '*', '.', '(', ')']:
                sigma.add(sym)
        _, dfa.auto = determinate(auto, list(sigma))
        return dfa

    @staticmethod
    def by_nfa(nfa: NFA, print_process: bool = False) -> 'DFA':
        if nfa.auto is None:
            return DFA()
        sigma = set()
        for vert in nfa.auto.vertices:
            for sym in vert.delta.keys():
                if sym != '':
                    sigma.add(sym)
        dfa = DFA()
        sigma = list(sigma)
        table, dfa.auto = determinate(nfa.auto, sigma)
        if print_process:
            print_determinization(table, sigma)
        return dfa

    def minimize(self, print_process: bool = False) -> 'DFA':
        if self.auto is None:
            return self
        sigma = set()
        for vert in self.auto.vertices:
            for sym in vert.delta.keys():
                if sym != '':
                    sigma.add(sym)
        sigma = list(sigma)
        make_complete(self.auto, sigma)
        tables, mini = minimize(self.auto, sigma)
        if print_process:
            print_minimization(tables, sigma)
        self.auto = mini
        return self

    def visualize(self):
        visualize_automaton(self.auto, 'DFA', True)

    def complement(self) -> 'DFA':
        if self.auto is None:
            return self
        sigma = set()
        for vert in self.auto.vertices:
            for sym in vert.delta.keys():
                if sym != '':
                    sigma.add(sym)
        sigma = list(sigma)
        make_complete(self.auto, sigma)
        complement(self.auto)
        return self
