'''Sequence class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement, c_export


class Sequence(NamedElement):

    __slots__ = ('_elements',)

    def __init__(self, *elements):
        self._elements = self._validate_elements(elements)

    def _get_node_result(self, root, tree, rule, _s, node):
        pos = node.start

        for elem in self._elements:
            is_valid, pos = root._walk(elem, pos, node.children, rule, True)
            if not is_valid:
                return is_valid, pos

        root._append_tree(tree, node, pos)

        return is_valid, pos

    def _run_export_js(self, js_identation, ident, classes):
        return self._export_js_elements(js_identation, ident, classes)

    def _run_export_c(self, c_identation, ident, enums):
        return self._export_c_elements(c_identation, ident, enums)