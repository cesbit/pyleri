import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Keyword,
)  # nopep8
from examples import JsonGrammar  # nopep8


class TestJsonLang(unittest.TestCase):

    def test_json(self):
        grammar = JsonGrammar()
        # should be true
        self.assertTrue(grammar.parse('''
            {
                "hoi \\"Iris\\"": [
                    5,
                    -0.5,
                    {
                        "a": true,
                        "b": false
                    }
                ]
            }''').is_valid)

        # keys must be strings
        self.assertFalse(grammar.parse('{5: true}').is_valid)

        # floats should start with 0-9.
        self.assertFalse(grammar.parse('{"a": .5}').is_valid)

        # wrong escaping
        self.assertFalse(grammar.parse('{"a\\": null}').is_valid)

        # empty strings are not allowed
        self.assertFalse(grammar.parse('').is_valid)


if __name__ == '__main__':
    unittest.main()
