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
    List
)  # nopep8


class TestList(unittest.TestCase):

    def test_list(self):
        k_hi = Keyword('hi')
        list_ = List(k_hi)
        grammar = create_grammar(list_)

        self.assertEqual(list_.min, 0)
        self.assertEqual(list_.max, None)
        self.assertFalse(list_.opt_closing)
        self.assertTrue(grammar.parse('hi, hi, hi').is_valid)
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertTrue(grammar.parse('').is_valid)
        self.assertFalse(grammar.parse('hi,').is_valid)
        self.assertEqual(
            str(grammar.parse('hi.')),
            'error at position 2, expecting: , or end_of_statement'
        )

    def test_list_all_options(self):
        k_hi = Keyword('hi')
        list_ = List(k_hi, delimiter='-', mi=1, ma=3, opt=True)
        grammar = create_grammar(list_)

        self.assertEqual(list_.min, 1)
        self.assertEqual(list_.max, 3)
        self.assertTrue(list_.opt_closing)

        self.assertTrue(grammar.parse('hi - hi - hi').is_valid)
        self.assertTrue(grammar.parse('hi-hi-hi-').is_valid)
        self.assertTrue(grammar.parse('hi-').is_valid)
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertFalse(grammar.parse('').is_valid)
        self.assertFalse(grammar.parse('-').is_valid)
        self.assertFalse(grammar.parse('hi-hi-hi-hi').is_valid)
        self.assertEqual(
            str(grammar.parse('hi-hi-hi-hi-hi')),
            'error at position 9, expecting: end_of_statement'
        )
        self.assertEqual(
            str(grammar.parse('hi.')),
            'error at position 2, expecting: - or end_of_statement'
        )
        self.assertEqual(
            str(grammar.parse('')),
            'error at position 0, expecting: hi'
        )


if __name__ == '__main__':
    unittest.main()
