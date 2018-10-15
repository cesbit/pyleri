import unittest
import os
import sys
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    KeywordError,
    create_grammar,
    Keyword,
    Ref,
)  # nopep8


class TestRef(unittest.TestCase):

    def test_ref(self):
        ref = Ref()
        k_hi = Keyword('HI')
        ref = k_hi
        grammar = create_grammar(ref)

        self.assertTrue(grammar.parse('HI').is_valid)
        self.assertFalse(grammar.parse('hi').is_valid)
        self.assertFalse(grammar.parse('').is_valid)
        self.assertEqual(
            str(grammar.parse('ha')),
            'error at position 0, expecting: HI',
        )


if __name__ == '__main__':
    unittest.main()
