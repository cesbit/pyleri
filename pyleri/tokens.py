'''Tokens class.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import NamedElement, c_export, go_export, java_export


class Tokens(NamedElement):

    __slots__ = ('_tokens',)

    def __init__(self, tokens):
        self._tokens = tokens.split()
        self._tokens.sort(key=len, reverse=True)

    def __repr__(self):
        return ' '.join(self._tokens)

    def _get_node_result(self, root, tree, rule, s, node):
        for token in self._tokens:
            if s.startswith(token):
                root._append_tree(tree, node, node.start + len(token))
                return True, node.end

        root._expecting.update(self, node.start)

        return False, node.start

    def _run_export_js(self, js_indent, indent, classes, cname):
        return 'Tokens(\'{}\')'.format(
            ' '.join(self._tokens).replace('\'', '\\\''))

    def _run_export_py(self, py_indent, indent, classes):
        return 'Tokens(\'{}\')'.format(
            ' '.join(self._tokens).replace('\'', '\\\''))

    @c_export
    def _run_export_c(self, c_indent, indent, enums, gid):
        return 'cleri_tokens({}, "{}")'.format(
            gid,
            ' '.join(self._tokens).replace('"', '\\"'))

    @go_export
    def _run_export_go(self, go_indent, indent, enums, gid):
        return 'goleri.NewTokens({}, "{}")'.format(
            gid,
            ' '.join(self._tokens).replace('"', '\\"'))

    @java_export
    def _run_export_java(self, java_indent, indent, enums, classes, gid):
        return 'new Tokens({}"{}")'.format(
            '' if gid is None else 'Ids.{}, '.format(gid),
            ' '.join(self._tokens).replace('"', '\\"'))
