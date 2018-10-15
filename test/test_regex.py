import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Regex,
)  # nopep8


class TestRegex(unittest.TestCase):

    def test_regex(self):
        regex = Regex('^(?:\'(?:[^\']*)\')+')
        grammar = create_grammar(regex)

        self.assertTrue(grammar.parse("'hi'").is_valid)
        self.assertTrue(grammar.parse("'this is ''SiriDB'''").is_valid)
        self.assertFalse(grammar.parse("'Hi !").is_valid)
        self.assertFalse(grammar.parse("'hello''").is_valid)
        self.assertFalse(grammar.parse("").is_valid)
        self.assertEqual(
            grammar.parse('hi.').as_str(
                translate=lambda elem: 'single_quoted_string'
                if elem is regex else None),
            'error at position 0, expecting: single_quoted_string'
        )


if __name__ == '__main__':
    unittest.main()
