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
    Regex,
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

    def test_choice_with_named_elements(self):
        int_value = Regex(r"\d+")
        int_value.name = "INT_VALUE"

        float_value = Regex(r"\d+(\.\d+)?")
        float_value.name = "FLOAT_VALUE"

        choice = Choice(float_value, int_value)
        grammar = create_grammar(choice)

        result = grammar.parse("invalid")

        expecting = {str(element) for element in result.expecting}

        self.assertIn('"INT_VALUE"', expecting)
        self.assertIn('"FLOAT_VALUE"', expecting)
        self.assertNotIn("Regex", expecting)


if __name__ == '__main__':
    unittest.main()
