import unittest
from interface.loader import load_automaton, save_automaton
from models.auto import Automaton, Vertex
from json import load
from pathlib import Path
from tests.helper import *


class TestLoader(unittest.TestCase):
    def test_save_json(self):
        q0 = Vertex(terminal=False, delta={}, index=0)
        q1 = Vertex(terminal=False, delta={}, index=1)
        q2 = Vertex(terminal=False, delta={}, index=2)
        q3 = Vertex(terminal=False, delta={}, index=3)
        q4 = Vertex(terminal=True, delta={}, index=4)
        q5 = Vertex(terminal=False, delta={}, index=5)
        q6 = Vertex(terminal=False, delta={}, index=6)
        q7 = Vertex(terminal=False, delta={}, index=7)
        q8 = Vertex(terminal=False, delta={}, index=8)

        q0.delta = {'': {q1, q7, q5}}
        q1.delta = {'a': {q2}}
        q2.delta = {'': {q3}}
        q3.delta = {'b': {q4}}
        q5.delta = {'a': {q6}}
        q6.delta = {'': {q0}}
        q7.delta = {'b': {q8}}
        q8.delta = {'': {q0}}

        vertices = {q0, q1, q2, q3, q4, q5, q6, q7, q8}
        auto = Automaton(start=q0, vertices=vertices)

        save_automaton(auto, 'test_loader.json')

        target_file = Path('tests/test_loader.json')
        with open(target_file, 'r') as f:
            target = load(f)

        target_file = Path('output/test_loader.json')
        with open(target_file, 'r') as f:
            got = load(f)

        self.assertEqual(target['s0'], got['s0'])
        self.assertTrue(compare_finals(target['final'], got['final']))
        self.assertTrue(compare_deltas(target['delta'], got['delta']))
        self.assertTrue(compare_states(target['states'], got['states']))


if __name__ == "__main__":
    unittest.main()
