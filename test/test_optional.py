import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Keyword,
    Optional,
)  # nopep8


class TestOptinal(unittest.TestCase):

    def test_optional(self):
        k_hi = Keyword('hi')
        optional = Optional(k_hi)
        grammar = create_grammar(optional)

        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertTrue(grammar.parse('').is_valid)
        self.assertFalse(grammar.parse('hello').is_valid)

        self.assertEqual(
            str(grammar.parse('hello')),
            'error at position 0, expecting: end_of_statement or hi'
        )
        self.assertEqual(
            str(grammar.parse('hi hi')),
            'error at position 2, expecting: end_of_statement'
        )


if __name__ == '__main__':
    unittest.main()
