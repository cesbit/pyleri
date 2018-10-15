import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Tokens,
)  # nopep8


class TestTokens(unittest.TestCase):

    def test_tokens(self):
        spaced = '== != >= <= > <'
        tokens = Tokens('== > !=  <  >=  <= ')
        grammar = create_grammar(tokens)

        self.assertEqual(spaced, str(tokens))
        self.assertTrue(grammar.parse('==').is_valid)
        self.assertTrue(grammar.parse('<=').is_valid)
        self.assertTrue(grammar.parse('>').is_valid)
        self.assertFalse(grammar.parse('').is_valid)
        self.assertFalse(grammar.parse('=').is_valid)
        self.assertEqual(
            str(grammar.parse('')),
            'error at position 0, expecting: == != >= <= > <'
        )


if __name__ == '__main__':
    unittest.main()
