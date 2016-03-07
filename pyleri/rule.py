'''Rule class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement


class Rule(NamedElement):

    __slots__ = ('_element', '_tested', '_tree')

    def __init__(self, element):
        self._element = element

    def _get_node_result(self, root, tree, rule, _s, node):
        self._tested = {}
        self._tree = {}
        is_valid, pos = root._walk(
            self._element,
            node.start,
            node.children,
            self,
            True)
        if is_valid:
            root._append_tree(tree, node, pos)
        return is_valid, pos

    def _run_export_js(self, js_identation, ident, classes):
        return self._element._export_js(js_identation, ident, classes)

    def _run_export_c(self, c_identation, ident, enums):
        name = getattr(self, 'name', None)
        if name is not None:
            self._element._name = name
        return self._element._export_c(c_identation, ident, enums)
