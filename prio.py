from .noderesult import NodeResult
from .elements import NamedElement
from .rule import Rule


class _Prio(NamedElement):

    __slots__ = ('_elements',)

    def __init__(self, *elements):
        self._elements = self._validate_elements(elements)

    def _get_node_result(self, root, tree, rule, s, node):
        if node.start not in rule._tested:
            rule._tested[node.start] = NodeResult(False, node.start)

        for elem in self._elements:
            children = []
            node_res = root._walk(elem, node.start, children, rule, True)
            if node_res.is_valid and \
                    node_res.pos > rule._tested[node.start].pos:
                node.children = rule._tree[node.start] = children
                rule._tested[node.start] = node_res

        if rule._tested[node.start].is_valid:
            root._append_tree(tree, node, rule._tested[node.start].pos)

        return rule._tested[node.start]

    def _run_export_js(self, js_identation, ident, classes):
        return self._export_js_elements(js_identation, ident, classes)

_Prio.__name__ = 'Prio'


def Prio(*elements):
    return Rule(_Prio(*elements))
