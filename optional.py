from .noderesult import NodeResult
from .elements import NamedElement


class Optional(NamedElement):

    __slots__ = ('_element',)

    def __init__(self, element):
        self._element = self._validate_element(element)

    def _get_node_result(self, root, tree, rule, s, node):
        node_res = root._walk(
            self._element,
            node.start,
            node.children,
            rule,
            False)
        if node_res.is_valid:
            root._append_tree(tree, node, node_res.pos)

        return NodeResult(True, node.end or node.start)

    def _new_export_js(self, js_identation, ident, classes):
        return 'Optional({})'.format(
            self._element._export_js(js_identation, ident, classes))
