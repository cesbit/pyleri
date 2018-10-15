import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Sequence,
    Keyword,
)  # nopep8


class TestSequence(unittest.TestCase):

    def test_sequence(self):
        k_hi = Keyword('hi')
        k_iris = Keyword('iris')
        seq = Sequence(k_hi, k_iris)
        grammar = create_grammar(seq)

        self.assertTrue(grammar.parse('hi iris').is_valid)
        self.assertFalse(grammar.parse(' hi sasha ').is_valid)
        self.assertEqual(
            str(grammar.parse('hi sasha')),
            'error at position 3, expecting: iris'
        )


if __name__ == '__main__':
    unittest.main()
