import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Keyword,
    Token,
    Choice,
)  # nopep8


class TestKeyword(unittest.TestCase):

    def test_keyword(self):
        k_hi = Keyword('hi')
        grammar = create_grammar(k_hi)

        self.assertFalse(k_hi.ign_case)
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertTrue(grammar.parse(' hi ').is_valid)
        self.assertFalse(grammar.parse('Hi').is_valid)
        self.assertFalse(grammar.parse('hello').is_valid)
        self.assertEqual(
            'error at position 0, expecting: hi',
            str(grammar.parse('hello')))
        self.assertEqual(
            'parsed successfully',
            str(grammar.parse('hi')))

    def test_keyword_ign_case(self):
        k_hi = Keyword('hi', ign_case=True)
        grammar = create_grammar(k_hi)

        self.assertTrue(k_hi.ign_case)
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertTrue(grammar.parse('Hi').is_valid)
        self.assertFalse(grammar.parse('hello').is_valid)
        self.assertEqual(
            'error at position 2, expecting: end_of_statement',
            str(grammar.parse('Hi Iris')))

    def test_keyword_alt_regkw(self):
        grammar = create_grammar(Choice(Keyword('hi'), Token('HI')), r'[a-z]+')
        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertTrue(grammar.parse('HI').is_valid)
        self.assertFalse(grammar.parse('').is_valid)
        self.assertFalse(grammar.parse('Hi').is_valid)


if __name__ == '__main__':
    unittest.main()
