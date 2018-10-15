import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Token,
)  # nopep8


class TestToken(unittest.TestCase):

    def test_token(self):
        dot = Token('.')
        grammar = create_grammar(dot)

        self.assertTrue(grammar.parse('.').is_valid)
        self.assertFalse(grammar.parse('..').is_valid)
        self.assertFalse(grammar.parse('').is_valid)
        self.assertEqual(
            str(grammar.parse('')),
            'error at position 0, expecting: .'
        )


if __name__ == '__main__':
    unittest.main()
