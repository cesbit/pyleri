from .noderesult import NodeResult
from .elements import NamedElement


class Repeat(NamedElement):

    __slots__ = ('_element', '_min', '_max')

    def __init__(self, element, mi=0, ma=None):
        self._element = self._validate_element(element)

        if not isinstance(mi, int) or mi < 0:
            raise TypeError('Repeat(): "mi" must be an integer value larger than or equal to 0, got: {}'.format(mi))

        self._min = mi

        if not isinstance(ma, (int, type(None))) or (ma is not None and ma < mi):
            raise TypeError('Repeat(): "ma" must be an integer or None value. If an integer is specified it must be larger than or equal to "mi"')

        self._max = ma

    def _get_node_result(self, root, tree, rule, s, node):
        pos, i = node.start, 0
        while not self._max or i < self._max:
            node_res = root._walk(self._element, pos, node.children, rule, i < self._min)
            if not node_res.is_valid:
                break
            pos = node_res.pos
            i += 1

        is_valid = i >= self._min
        if is_valid:
            root._append_tree(tree, node, pos)

        return NodeResult(is_valid, pos)

    def _new_export_js(self, js_identation, ident, classes):
        return 'Repeat({}, {}, {})'.format(
            self._element._export_js(js_identation, ident, classes),
            self._min,
            self._max or 'undefined')
