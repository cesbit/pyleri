'''Prio class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement
from .rule import Rule


class _Prio(NamedElement):

    __slots__ = ('_elements', '_name')

    def __init__(self, *elements):
        self._elements = self._validate_elements(elements)

    def _get_node_result(self, root, tree, rule, s, node):
        if node.start not in rule._tested:
            rule._tested[node.start] = False, node.start

        for elem in self._elements:
            children = []
            is_valid, pos = root._walk(elem, node.start, children, rule, True)
            if is_valid and \
                    pos > rule._tested[node.start][1]:
                node.children = rule._tree[node.start] = children
                rule._tested[node.start] = is_valid, pos

        if rule._tested[node.start][0]:
            root._append_tree(tree, node, rule._tested[node.start][1])

        return rule._tested[node.start]

    def _run_export_js(self, js_identation, ident, classes):
        return self._export_js_elements(js_identation, ident, classes)

    def _run_export_c(self, c_identation, ident, enums):
        return self._export_c_elements(c_identation, ident, enums)

_Prio.__name__ = 'Prio'


def Prio(*elements):
    return Rule(_Prio(*elements))
