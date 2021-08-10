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
    Prio,
    List,
    THIS,
    MaxRecursionError,
)  # nopep8


class TestPrio(unittest.TestCase):

    def test_prio(self):
        k_hi = Keyword('hi')
        k_bye = Keyword('bye')
        k_and = Keyword('and')
        k_or = Keyword('or')
        prio = Prio(
            k_hi,
            k_bye,
            Sequence('(', THIS, ')'),
            Sequence(THIS, k_and, THIS),
            Sequence(THIS, k_or, THIS),
        )
        grammar = create_grammar(prio)

        self.assertTrue(grammar.parse('hi').is_valid)
        self.assertTrue(grammar.parse('(bye)').is_valid)
        self.assertTrue(grammar.parse('(hi and bye)').is_valid)
        self.assertTrue(grammar.parse('(hi or hi) and (hi or hi)').is_valid)
        self.assertTrue(grammar.parse('(hi or (hi and bye))').is_valid)
        self.assertFalse(grammar.parse('').is_valid)
        self.assertFalse(grammar.parse('(hi').is_valid)
        self.assertFalse(grammar.parse('()').is_valid)
        self.assertFalse(grammar.parse('(hi or hi) and').is_valid)
        with self.assertRaises(MaxRecursionError):
            grammar.parse(
                '(((((((((((((((((((((((((((((((((((((((((((((((((((hi'
                ')))))))))))))))))))))))))))))))))))))))))))))))))))'
            )

    def test_prio_list(self):
        arr = Sequence('[', List(THIS), ']')
        prio = Prio(Keyword('nil'), arr)
        grammar = create_grammar(prio)
        self.assertTrue(grammar.parse('[]').is_valid)
        self.assertTrue(grammar.parse('[[nil]]').is_valid)
        self.assertTrue(
            grammar.parse(
                '['
                'nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,'
                'nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,'
                'nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,'
                'nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,'
                'nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,'
                'nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil,nil'
                ']').is_valid)
        with self.assertRaises(MaxRecursionError):
            grammar.parse(
                '[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[hi'
                ']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]'
            )


if __name__ == '__main__':
    unittest.main()
