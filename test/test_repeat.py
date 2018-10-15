import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Sequence,
    Choice,
    Keyword,
    Token,
    Repeat,
)  # nopep8


class TestRepeat(unittest.TestCase):

    def test_repeat(self):
        k_hi = Keyword('hi')
        repeat = Repeat(k_hi)
        grammar = create_grammar(repeat)

        self.assertEqual(repeat.min, 0)
        self.assertEqual(repeat.max, None)
        self.assertTrue(grammar.parse('hi hi hi').is_valid)
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertTrue(grammar.parse('').is_valid)
        self.assertFalse(grammar.parse('hihi').is_valid)
        self.assertFalse(grammar.parse('ha,').is_valid)
        self.assertEqual(
            grammar.parse('hi.').as_str(),
            'error at position 2, expecting: end_of_statement or hi'
        )
        self.assertEqual(
            grammar.parse('hi.').as_str(translate=lambda elem: ''),
            'error at position 2'
        )

    def test_repeat_all_options(self):
        k_hi = Keyword('hi')
        repeat = Repeat(k_hi, mi=1, ma=3)
        grammar = create_grammar(repeat)

        self.assertEqual(repeat.min, 1)
        self.assertEqual(repeat.max, 3)
        self.assertTrue(grammar.parse('hi hi hi').is_valid)
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertFalse(grammar.parse('').is_valid)
        self.assertFalse(grammar.parse('hi hi hi hi').is_valid)
        self.assertEqual(
            grammar.parse('hi hi hi hi hi.').as_str(),
            'error at position 8, expecting: end_of_statement'
        )
        self.assertEqual(
            grammar.parse('hi.').as_str(),
            'error at position 2, expecting: end_of_statement or hi'
        )
        self.assertEqual(
            grammar.parse('').as_str(),
            'error at position 0, expecting: hi'
        )


if __name__ == '__main__':
    unittest.main()
