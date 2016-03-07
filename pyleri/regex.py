'''Regex class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
import re
from .elements import NamedElement, c_export


class Regex(NamedElement):

    __slots__ = ('_compiled',)

    def __init__(self, pattern, flags=0):
        if not pattern.startswith('^'):
            pattern = '^' + pattern
        self._compiled = re.compile(pattern, flags=flags)

    def __repr__(self):
        name = getattr(self, 'name', None)
        return self.__class__.__name__ if name is None else '"{}"'.format(name)

    def _get_node_result(self, root, tree, rule, s, node):
        re_match = self._compiled.match(s)
        is_valid = bool(re_match)

        if is_valid:
            root._append_tree(tree, node, node.start + len(re_match.group(0)))
        else:
            root._expecting.update(self, node.start)

        return is_valid, node.end or node.start

    def _run_export_js(self, js_identation, ident, classes):
        return 'Regex(\'{}\')'.format(
            self._compiled.pattern.replace('\\', '\\\\').replace('\'', '\\\''))

    @c_export
    def _run_export_c(self, c_identation, ident, enums, gid):
        return 'cleri_regex({}, "{}")'.format(
            gid,
            self._compiled.pattern
                .replace('\\', '\\\\')
                .replace('\'', '\\\'')
                .replace('\\"', '"')
                .replace('"', '\\"'))
