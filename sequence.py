'''Sequence class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement


class Sequence(NamedElement):

    __slots__ = ('_elements',)

    def __init__(self, *elements):
        self._elements = self._validate_elements(elements)

    def _get_node_result(self, root, tree, rule, s, node):
        pos = node.start

        for elem in self._elements:
            is_valid, p = root._walk(elem, pos, node.children, rule, True)
            if is_valid:
                pos = p
            else:
                return is_valid, p

        root._append_tree(tree, node, p)

        return is_valid, p

    def _run_export_js(self, js_identation, ident, classes):
        return self._export_js_elements(js_identation, ident, classes)
