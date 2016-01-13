'''Rule class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement


class Rule(NamedElement):

    __slots__ = ('_element', '_tested', '_tree')

    def __init__(self, element):
        self._element = element

#     @property
#     def _elements(self):
#         yield self._element

    def _get_node_result(self, root, tree, rule, s, node):
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
