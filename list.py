'''pyleri.List Class.

The grammar must find given elements separated by a delimiter. When no delimiter
is given we split using a comma. All arguments:

    element: List searches for this element
    delimiter: Elements must be separated by this delimiter. (default: ',')
    mi: Minimal elements the parser will search for. (default: 0)
    ma: Maximum elements the parser will search for. (default: None, unlimited)
    opt: When set to True the list may end with a delimiter. (default: False)

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
:license: need to decide
'''

from .noderesult import NodeResult
from .elements import NamedElement


class List(NamedElement):

    __slots__ = ('_element', '_delimiter', '_min', '_max', '_opt')

    def __init__(self, element, delimiter=',', mi=0, ma=None, opt=False):
        self._element, self._delimiter = map(self._validate_element, (element, delimiter))

        if not isinstance(mi, int) or mi < 0:
            raise TypeError('Repeat(): "mi" must be an integer value larger than or equal to 0, got: {}'.format(mi))
        self._min = mi

        if not isinstance(ma, (int, type(None))) or (ma is not None and ma < mi):
            raise TypeError('Repeat(): "ma" must be an integer or None value. If an integer is specified it must be larger than or equal to "mi"')
        self._max = ma

        self._opt = bool(opt)  # When opt is True the list may end with a delimiter

    def _get_node_result(self, root, tree, rule, s, node):
        pos, i, j = node.start, 0, 0
        while True:
            node_res = root._walk(self._element, pos, node.children, rule, i < self._min)
            if not node_res.is_valid:
                break
            pos = node_res.pos
            i += 1

            node_res = root._walk(self._delimiter, pos, node.children, rule, i < self._min)
            if not node_res.is_valid:
                break
            pos = node_res.pos
            j += 1

        is_valid = not (i < self._min or (self._max and i > self._max) or (not self._opt and i and i == j))
        if is_valid:
            root._append_tree(tree, node, pos)

        return NodeResult(is_valid, pos)

    def _new_export_js(self, js_identation, ident, classes):
        return 'List({}, {}, {}, {}, {})'.format(
            self._element._export_js(js_identation, ident, classes),
            self._delimiter._export_js(js_identation, ident, classes),
            self._min,
            self._max or 'undefined',
            'true' if self._opt else 'false')
