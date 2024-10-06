import unittest
from operations.poland import to_polish_notation


class TestPolishNotation(unittest.TestCase):
    def test_obvious(self):
        regex = "((ab+bb)*+a*)ba"
        expected_result = "ab.bb.+*a*+b.a."
        result = to_polish_notation(regex)
        self.assertEqual(result, expected_result, "Polish notation is incorrect")

    def test_epsilon(self):
        regex = "(_+_*)*___*"
        expected_result = "__*+*_._._*."
        result = to_polish_notation(regex)
        self.assertEqual(result, expected_result, "Polish notation with epsilon is incorrect")


if __name__ == "__main__":
    unittest.main()
