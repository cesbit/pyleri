import unittest
import sys
import os
if os.environ.get('USELIB') != '1':
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyleri import (
    Grammar,
    Keyword,
    KeywordError,
    MissingStartError,
    NameAssignedError,
    Optional,
    ReKeywordsChangedError,
    UnusedElementError,
    create_grammar,
)  # nopep8
from examples import JsonGrammar  # nopep8


class TestCompile(unittest.TestCase):

    def test_compile_error(self):
        with self.assertRaises(ReKeywordsChangedError):
            class _G1(Grammar):
                k_test = Keyword('test')
                RE_KEYWORDS = '^[a-z]+'

        with self.assertRaises(KeywordError):
            class _G2(Grammar):
                k_test = Keyword('test-nomatch')

        with self.assertRaises(KeywordError):
            # test 'deep' keyword checks.
            class _G3(Grammar):
                START = Optional(Keyword('test-nomatch'))

        with self.assertRaises(NameAssignedError):
            class _G4(Grammar):
                k_test = Keyword('test')
                k_test2 = k_test

        with self.assertRaises(NameAssignedError):
            class _G5(Grammar):
                k_test = Keyword('test')
                k_Test = Keyword('duplicate')

        with self.assertRaises(MissingStartError):
            class _G6(Grammar):
                k_test = Keyword('test')

        with self.assertRaises(UnusedElementError):
            class _G7(Grammar):
                k_test = Keyword('test')
                START = Keyword('bla')

    def test_compile(self):
        class _G1(Grammar):
            k_hi = Keyword('hi')
            START = Optional(k_hi)

        self.assertEqual(_G1.k_hi.name, 'k_hi')


if __name__ == '__main__':
    unittest.main()
