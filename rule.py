from .elements import NamedElement


class Rule(NamedElement):

    __slots__ = ('_element', '_tested', '_tree')

    def __init__(self, element):
        self._element = element

    @property
    def _elements(self):
        yield self._element

    def _get_node_result(self, root, tree, rule, s, node):
        self._tested = {}
        self._tree = {}
        node_res = root._walk(
            self._element,
            node.start,
            node.children,
            self,
            True)
        if node_res.is_valid:
            root._append_tree(tree, node, node_res.pos)
        return node_res

    def _new_export_js(self, js_identation, ident, classes):
        return self._element._export_js(js_identation, ident, classes)
