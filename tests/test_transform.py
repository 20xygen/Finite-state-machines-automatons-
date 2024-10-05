import unittest
from operations.poland import polska_into_auto
from models.auto import Automaton, Vertex
from interface.loader import save_automaton
from pathlib import Path
from json import load
from helper import *
from operations.transform import determinate, minimize, make_complete, complement
from typing import List
from operations.regexify import to_regex


class TestTransform(unittest.TestCase):
    def test_determinate(self):
        # tested section:
        sigma = ['a', 'b']
        polish_notation = "ab+*a.b."
        auto = polska_into_auto(polish_notation)

        _, det = determinate(auto, sigma)
        save_automaton(det, 'test_determinization.json')

        file = Path('output/test_determinization.json')
        with open(file, 'r') as f:
            got = load(f)

        target_file = Path('tests/test_determinization.json')
        with open(target_file, 'r') as f:
            target = load(f)

        self.assertEqual(target['s0'], got['s0'])
        self.assertTrue(compare_finals(target['final'], got['final']))
        self.assertTrue(compare_deltas(target['delta'], got['delta']))
        self.assertTrue(compare_states(target['states'], got['states']))

    def test_fulfill(self):
        # tested section:
        sigma = ['a', 'b']
        polish_notation = "ab+*a.b."
        auto = polska_into_auto(polish_notation)
        _, det = determinate(auto, sigma)

        make_complete(det, sigma)
        save_automaton(det, 'test_full.json')

        file = Path('output/test_full.json')
        with open(file, 'r') as f:
            got = load(f)

        target_file = Path('tests/test_full.json')
        with open(target_file, 'r') as f:
            target = load(f)

        self.assertEqual(target['s0'], got['s0'])
        self.assertTrue(compare_finals(target['final'], got['final']))
        self.assertTrue(compare_deltas(target['delta'], got['delta']))
        self.assertTrue(compare_states(target['states'], got['states']))

    def test_minimize(self):
        # tested section:
        sigma = ['a', 'b']
        polish_notation = "ab+*a.b."
        auto = polska_into_auto(polish_notation)
        _, det = determinate(auto, sigma)
        make_complete(det, sigma)

        _, mini = minimize(det, sigma)
        save_automaton(mini, 'test_mini.json')

        file = Path('output/test_mini.json')
        with open(file, 'r') as f:
            got = load(f)

        target_file = Path('tests/test_mini.json')
        with open(target_file, 'r') as f:
            target = load(f)

        self.assertEqual(target['s0'], got['s0'])
        self.assertTrue(compare_finals(target['final'], got['final']))
        self.assertTrue(compare_deltas(target['delta'], got['delta']))
        self.assertTrue(compare_states(target['states'], got['states']))

    def test_regex(self):
        # tested section:
        sigma = ['a', 'b']
        polish_notation = "ab+*a.b."
        auto = polska_into_auto(polish_notation)
        _, det = determinate(auto, sigma)
        make_complete(det, sigma)
        _, mini = minimize(det, sigma)

        rx = to_regex(mini)
        self.assertEqual(rx, "((b+aa*b(aa*b)*b)*)aa*b(aa*b)*")

    def test_invert(self):
        # tested section:
        sigma = ['a', 'b']
        polish_notation = "ab+*a.b."
        auto = polska_into_auto(polish_notation)
        _, det = determinate(auto, sigma)
        make_complete(det, sigma)
        _, mini = minimize(det, sigma)

        complement(mini)
        save_automaton(mini, 'test_invert.json')

        file = Path('output/test_invert.json')
        with open(file, 'r') as f:
            got = load(f)

        target_file = Path('tests/test_invert.json')
        with open(target_file, 'r') as f:
            target = load(f)

        self.assertEqual(target['s0'], got['s0'])
        self.assertTrue(compare_finals(target['final'], got['final']))
        self.assertTrue(compare_deltas(target['delta'], got['delta']))
        self.assertTrue(compare_states(target['states'], got['states']))


if __name__ == "__main__":
    unittest.main()
