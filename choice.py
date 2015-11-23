'''pyleri.Choice Class.

Choose one of the given elements. When most_greedy is True we will choose
the 'longest' element when multiple elements are valid. If most_greedy is
False we will return the first match.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''

from .noderesult import NodeResult
from .elements import NamedElement


class Choice(NamedElement):

    __slots__ = ('_elements', '_get_node_result')

    def __init__(self, *elements, most_greedy=True):
        self._elements = self._validate_elements(elements)
        self._get_node_result = \
            self._most_greedy_result if most_greedy else \
            self._stop_at_first_match

    def _most_greedy_result(self, root, tree, rule, s, node):
        most_greedy = NodeResult(False, node.start)

        for elem in self._elements:
            children = []
            node_res = root._walk(elem, node.start, children, rule, True)

            if node_res.is_valid and node_res.pos > most_greedy.pos:
                node.children = children
                most_greedy = node_res

        if most_greedy.is_valid:
            root._append_tree(tree, node, most_greedy.pos)

        return most_greedy

    def _stop_at_first_match(self, root, tree, rule, s, node):
        for elem in self._elements:
            children = []
            node_res = root._walk(elem, node.start, children, rule, True)

            if node_res.is_valid:
                node.children = children
                root._append_tree(tree, node, node_res.pos)
                break

        return node_res

    def _run_export_js(self, js_identation, ident, classes):
        return self._export_js_elements(js_identation, ident, classes)
