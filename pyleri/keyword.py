'''pyleri.Keyword Class.

Try matching a given keyword string. The keyword should match
Grammer.RE_KEYWORDS otherwise the keyword will not be found. It's possible
however to overwrite the default RE_KEYWORDS in you own Grammar class.

Example:

class MyGrammar(Grammar):

    # needed because the default ^\w+ will not match keyword: my-keyword
    RE_KEYWORDS = re.compile('^[\w-]+')

    my_keyword = Keyword('my-keyword')
    ...


:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement, c_export


class Keyword(NamedElement):

    __slots__ = ('_keyword', '_ign_case')

    def __init__(self, keyword, ign_case=False):

        if not isinstance(keyword, str):
            raise TypeError(
                'Keyword(): first positional argument must be a string value')

        self._keyword = keyword
        self._ign_case = bool(ign_case)

    def __repr__(self):
        return self._keyword

    def _get_node_result(self, root, tree, rule, s, node):
        try:
            re_match = root._cached_kw_match[node.start]
        except KeyError:
            re_match = \
                root._cached_kw_match[node.start] = \
                root.RE_KEYWORDS.match(s)
        is_valid = \
            re_match and \
            (re_match.group(0) == self._keyword or
             (self._ign_case and
              re_match.group(0).lower() == self._keyword.lower()))
        if is_valid:
            root._append_tree(tree, node, node.start + len(self._keyword))
        else:
            root._expecting.update(self, node.start)

        return is_valid, node.end or node.start

    def _run_export_js(self, js_identation, ident, classes):
        return 'Keyword(\'{}\'{})'.format(
            self._keyword,
            ', true' if self._ign_case else '')

    @c_export
    def _run_export_c(self, c_identation, ident, enums, gid):
        return 'cleri_keyword({}, "{}", {})'.format(
            gid,
            self._keyword,
            'CLERI_CASE_INSENSITIVE'
            if self._ign_case else 'CLERI_CASE_INSENSITIVE')
