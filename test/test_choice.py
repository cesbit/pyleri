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
)  # nopep8


class TestChoice(unittest.TestCase):

    def test_choice_most_greedy(self):
        k_hi = Keyword('hi')
        k_iris = Keyword('iris')
        seq = Sequence(k_hi, k_iris)
        choice = Choice(k_hi, seq)
        grammar = create_grammar(choice)

        self.assertTrue(choice.most_greedy)
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertTrue(grammar.parse(' hi iris ').is_valid)
        self.assertFalse(grammar.parse(' hi sasha ').is_valid)

    def test_choice_first_match(self):
        k_hi = Keyword('hi')
        k_iris = Keyword('iris')
        seq = Sequence(k_hi, k_iris)
        choice = Choice(k_hi, seq, most_greedy=False)
        grammar = create_grammar(choice)

        self.assertFalse(choice.most_greedy)
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertFalse(grammar.parse(' hi iris ').is_valid)
        self.assertFalse(grammar.parse(' hi sasha ').is_valid)


if __name__ == '__main__':
    unittest.main()
