import unittest
import gc
from pyleri import (
    Keyword,
    Sequence,
    Optional,
    Prio,
    THIS,
    Grammar,
    KeywordError,
    ReKeywordsChangedError,
    NameAssignedError)


class _TestGrammar1(Grammar):
    k_test = Keyword('test')
    k_ignore_case = Keyword('ignore_case', ign_case=True)
    START = Sequence(k_test, k_ignore_case)


class _TestGrammar2(Grammar):
    START = Prio(
        Keyword('ni'),
        Sequence('(', THIS, ')'),
        Sequence(THIS, Keyword('and'), THIS),
        Sequence(THIS, Keyword('or'), THIS))


class TestPyleri(unittest.TestCase):

    def setUp(self):
        gc.collect()

    def test_parse_keyword(self):
        tg = _TestGrammar1()
        self.assertTrue(tg.parse('test ignore_case').is_valid)
        self.assertTrue(tg.parse('test Ignore_Case').is_valid)
        self.assertFalse(tg.parse('Test ignore_case').is_valid)
        self.assertFalse(tg.parse('test ignore-case').is_valid)

    def test_noderesult_from_sequence(self):
        tg = _TestGrammar1()
        k_test, k_ignore_case = tg.parse(
                'test ignore_case').tree.children[0].children
        # element should be the original element
        self.assertEqual(k_test.element, _TestGrammar1.k_test)

        # Keyword string should be equal to str(Keyword)
        self.assertEqual(k_test.string, str(_TestGrammar1.k_test))

        # Test second node result
        self.assertEqual(k_ignore_case.element, _TestGrammar1.k_ignore_case)

    def test_compile_error(self):
        with self.assertRaises(ReKeywordsChangedError):
            class _G1(Grammar):
                k_test = Keyword('test')
                RE_KEYWORDS = '[a-z]+'

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

    def test_prio(self):
        tg = _TestGrammar2()
        self.assertTrue(tg.parse('ni').is_valid)
        self.assertTrue(tg.parse('(ni)').is_valid)
        self.assertTrue(tg.parse('ni and ni').is_valid)
        self.assertTrue(tg.parse('((ni) and ni and (ni or ni))').is_valid)
        self.assertFalse(tg.parse('(ni or ni and ni').is_valid)
        self.assertFalse(tg.parse('ni (ni)').is_valid)

    def tearDown(self):
        self.assertEqual(gc.collect(), 0, msg=self.id())


if __name__ == '__main__':
    unittest.main()
