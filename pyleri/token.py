'''Token class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement, c_export


class Token(NamedElement):

    __slots__ = ('_token',)

    def __init__(self, token):
        if not isinstance(token, str):
            raise TypeError('Token(): first argument must be a string '
                            'value, got {}'.format(token))
        self._token = token

    def __repr__(self):
        return self._token

    def _get_node_result(self, root, tree, rule, s, node):
        is_valid = s.startswith(self._token)

        if is_valid:
            root._append_tree(tree, node, node.start + len(self._token))
        else:
            root._expecting.update(self, node.start)

        return is_valid, node.end or node.start

    def _run_export_js(self, js_identation, ident, classes):
        return 'Token(\'{}\')'.format(self._token)

    @c_export
    def _run_export_c(self, js_identation, ident, enums, gid):
        return 'cleri_token({}, "{}")'.format(
            gid,
            self._token)
