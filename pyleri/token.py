'''Token class.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import NamedElement, c_export, go_export, java_export


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

    def _run_export_js(self, js_indent, indent, classes, cname):
        return 'Token(\'{}\')'.format(self._token.replace('\'', '\\\''))

    def _run_export_py(self, py_indent, indent, classes):
        return 'Token(\'{}\')'.format(self._token.replace('\'', '\\\''))

    @c_export
    def _run_export_c(self, js_indent, indent, enums, gid):
        return 'cleri_token({}, "{}")'.format(
            gid,
            self._token.replace('"', '\\"'))

    @go_export
    def _run_export_go(self, go_indent, indent, enums, gid):
        return 'goleri.NewToken({}, "{}")'.format(
            gid,
            self._token.replace('"', '\\"'))

    @java_export
    def _run_export_java(self, java_indent, indent, enums, classes, gid):
        return 'new Token({}"{}")'.format(
            '' if gid is None else 'Ids.{}, '.format(gid),
            self._token.replace('"', '\\"'))
