'''Tokens class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement, c_export


class Tokens(NamedElement):

    __slots__ = ('_tokens',)

    def __init__(self, tokens):
        self._tokens = tokens.split()
        self._tokens.sort(key=len, reverse=True)

    def __repr__(self):
        return ', '.join(self._tokens)

    def _get_node_result(self, root, tree, rule, s, node):
        for token in self._tokens:
            if s.startswith(token):
                root._append_tree(tree, node, node.start + len(token))
                return True, node.end

        root._expecting.update(self, node.start)

        return False, node.start

    def _run_export_js(self, js_identation, ident, classes):
        return 'Tokens(\'{}\')'

    @c_export
    def _run_export_c(self, c_identation, ident, enums, gid):
        return 'cleri_tokens({}, "{}")'.format(
            gid,
            ' '.join(self._tokens))
