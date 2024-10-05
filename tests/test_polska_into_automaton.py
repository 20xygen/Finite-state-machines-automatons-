import unittest
from operations.poland import polska_into_auto
from models.auto import Automaton, Vertex
from operations.transform import sign
from interface.loader import save_automaton
from pathlib import Path
from json import load
from helper import *


class TestPolskaIntoAutomaton(unittest.TestCase):
    def test(self):
        polish_notation = "ab+*a.b."
        auto = polska_into_auto(polish_notation)
        sign(auto)

        save_automaton(auto, 'test_polska.json')
        file = Path('output/test_loader.json')
        with open(file, 'r') as f:
            got = load(f)

        target_file = Path('tests/test_loader.json')
        with open(target_file, 'r') as f:
            target = load(f)

        self.assertEqual(target['s0'], got['s0'])
        self.assertTrue(compare_finals(target['final'], got['final']))
        self.assertTrue(compare_deltas(target['delta'], got['delta']))
        self.assertTrue(compare_states(target['states'], got['states']))


if __name__ == "__main__":
    unittest.main()
