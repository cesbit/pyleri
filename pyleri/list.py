'''pyleri.List Class.

The grammar must find given elements separated by a delimiter. When no
delimiter is given we split using a comma. All arguments:

    element: List searches for this element
    delimiter: Elements must be separated by this delimiter. (default: ',')
    mi: Minimal elements the parser will search for. (default: 0)
    ma: Maximum elements the parser will search for. (default: None, unlimited)
    opt: When set to True the list may end with a delimiter. (default: False)

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement, c_export


class List(NamedElement):

    __slots__ = ('_element', '_delimiter', '_min', '_max', '_opt')

    def __init__(self, element, delimiter=',', mi=0, ma=None, opt=False):
        self._element, self._delimiter = \
            map(self._validate_element, (element, delimiter))

        if not isinstance(mi, int) or mi < 0:
            raise TypeError('Repeat(): "mi" must be an integer value larger '
                            'than or equal to 0, got: {}'.format(mi))
        self._min = mi

        if not isinstance(ma, (int, type(None))) or \
                (ma is not None and ma < mi):
            raise TypeError('Repeat(): "ma" must be an integer or None value. '
                            'If an integer is specified it must be larger '
                            'than or equal to "mi"')
        self._max = ma

        # When opt is True the list may end with a delimiter
        self._opt = bool(opt)

    @property
    def _elements(self):
        yield self._element
        yield self._delimiter

    def _get_node_result(self, root, tree, rule, s, node):
        pos, i, j = node.start, 0, 0
        while True:
            is_valid, p = root._walk(
                self._element,
                pos,
                node.children,
                rule,
                i < self._min)
            if not is_valid:
                break
            pos = p
            i += 1

            is_valid, p = root._walk(
                self._delimiter,
                pos,
                node.children,
                rule,
                i < self._min)
            if not is_valid:
                break
            pos = p
            j += 1

        is_valid = not (i < self._min or
                        (self._max and
                         i > self._max) or
                        (not self._opt and
                         i and
                         i == j))
        if is_valid:
            root._append_tree(tree, node, pos)

        return is_valid, pos

    def _run_export_js(self, js_identation, ident, classes):
        return 'List({}, {}, {}, {}, {})'.format(
            self._element._export_js(js_identation, ident, classes),
            self._delimiter._export_js(js_identation, ident, classes),
            self._min,
            self._max or 'undefined',
            'true' if self._opt else 'false')

    @c_export
    def _run_export_c(self, c_identation, ident, enums, gid):
        return 'cleri_list({}, {}, {}, {}, {}, {})'.format(
            gid,
            self._element._export_c(c_identation, ident, enums),
            self._delimiter._export_c(c_identation, ident, enums),
            self._min,
            self._max or '0',
            '1' if self._opt else '0')
