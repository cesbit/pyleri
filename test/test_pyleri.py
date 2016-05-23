import unittest
import gc
import sys
sys.path.append('../')
from pyleri import (
    Keyword,
    Sequence,
    Optional,
    Regex,
    Prio,
    Choice,
    THIS,
    Ref,
    List,
    Repeat,
    Grammar,
    KeywordError,
    ReKeywordsChangedError,
    NameAssignedError)


class _TestGrammar1(Grammar):
    k_test = Keyword('test')
    k_ignore_case = Keyword('ignore_case', ign_case=True)
    START = Sequence(k_test, k_ignore_case)


class _TestGrammar2(Grammar):
    k_ni = Keyword('ni');
    s_seq = Sequence('(', THIS, ')');
    START = Prio(
        k_ni,
        s_seq,
        Sequence(THIS, Keyword('and'), THIS),
        Sequence(THIS, Keyword('or'), THIS))


class _TestGrammar3(Grammar):
    s_tic_tac = Sequence(Keyword('tic'), Keyword('tac'))
    s_tic_tac_toe = Sequence(Keyword('tic'), Keyword('tac'), Keyword('toe'))

    START = Sequence(
        Choice(s_tic_tac, s_tic_tac_toe),
        Choice(s_tic_tac, s_tic_tac_toe, most_greedy=False))


class _TestGrammar4(Grammar):
    START = Ref()
    ni_item = Choice(Keyword('ni'), START)
    START = Sequence('[', List(ni_item), ']')


class JsonGrammar(Grammar):
    START = Ref()

    # JSON strings should be enclosed in double quoates.
    # A backslash can be used as escape character.
    r_string = Regex('(")(?:(?=(\\\?))\\2.)*?\\1')

    # JSON does not support floats or integers prefixed with a + sign
    # and floats must start with a number, for example .5 is not allowed
    # but should be written like 0.5
    r_float = Regex('-?[0-9]+\.?[0-9]+')
    r_integer = Regex('-?[0-9]+')

    k_true = Keyword('true')
    k_false = Keyword('false')
    k_null = Keyword('null')

    json_map_item = Sequence(r_string, ':', START)

    json_map = Sequence('{', List(json_map_item), '}')
    json_array = Sequence('[', List(START), ']')

    START = Choice(
        r_string,
        r_float,
        r_integer,
        k_true,
        k_false,
        k_null,
        json_map,
        json_array)


class TestPyleri(unittest.TestCase):

    def setUp(self):
        gc.collect()

    def test_parse_keyword(self):
        tg = _TestGrammar1()
        self.assertTrue(tg.parse('test ignore_case').is_valid)
        self.assertTrue(tg.parse('test Ignore_Case').is_valid)
        # test is not case insensitive
        self.assertFalse(tg.parse('Test ignore_case').is_valid)
        # - is not _
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
        # missing closing )
        self.assertFalse(tg.parse('(ni or ni and ni').is_valid)
        # missing and/or between ni and (ni)
        self.assertFalse(tg.parse('ni (ni)').is_valid)

    def test_choice(self):
        tg = _TestGrammar3()
        # both should stop at first match
        self.assertTrue(tg.parse('tic tac tic tac').is_valid)
        # tic tac toe should be matched because most_greede is left default
        # (True) for the first choice
        self.assertTrue(tg.parse('tic tac toe tic tac').is_valid)
        # the second tic tac toe should NOT be matched because most_greede is
        # set to False for the second choice
        self.assertFalse(tg.parse('tic tac toe tic tac toe').is_valid)

    def test_ref(self):
        tg = _TestGrammar4()
        # should be true
        self.assertTrue(tg.parse('[ni, ni, [ni, [], [ni, ni]]]').is_valid)

    def test_json(self):
        tg = JsonGrammar()
        # should be true
        self.assertTrue(tg.parse('''
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
        self.assertFalse(tg.parse('{5: true}').is_valid)

        # floats should start with 0-9.
        self.assertFalse(tg.parse('{"a": .5}').is_valid)

        # wrong escaping
        self.assertFalse(tg.parse('{"a\\": null}').is_valid)

        # empty strings are not allowed
        self.assertFalse(tg.parse('').is_valid)

    def tearDown(self):
        self.assertEqual(gc.collect(), 0, msg=self.id())


if __name__ == '__main__':
    # unittest.main()

    grammar = JsonGrammar()
    print(grammar.export_c()[0])