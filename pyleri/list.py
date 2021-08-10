'''pyleri.List Class.

The grammar must find given elements separated by a delimiter. When no
delimiter is given we split using a comma. All arguments:

    element: List searches for this element
    delimiter: Elements must be separated by this delimiter. (default: ',')
    mi: Minimal elements the parser will search for. (default: 0)
    ma: Maximum elements the parser will search for. (default: None, unlimited)
    opt: When set to True the list may end with a delimiter. (default: False)

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import NamedElement, c_export, go_export, java_export


class List(NamedElement):

    __slots__ = ('_element', '_delimiter', '_min', '_max', '_opt')

    def __init__(self, element, delimiter=',', mi=0, ma=None, opt=False):
        self._element, self._delimiter = \
            map(self._validate_element, (element, delimiter))

        if not isinstance(mi, int) or mi < 0:
            raise TypeError('List(): "mi" must be an integer value larger '
                            'than or equal to 0, got: {}'.format(mi))
        self._min = mi

        if not isinstance(ma, (int, type(None))) or \
                (ma is not None and ma < mi):
            raise TypeError('List(): "ma" must be an integer or None value. '
                            'If an integer is specified it must be larger '
                            'than or equal to "mi"')
        self._max = ma

        # When opt is True the list may end with a delimiter
        self._opt = bool(opt)

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def opt_closing(self):
        return self._opt

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
            i += 1
            pos = p
            if i == self._max and not self._opt:
                break

            is_valid, p = root._walk(
                self._delimiter,
                pos,
                node.children,
                rule,
                i < self._min)
            if not is_valid:
                break
            j += 1
            pos = p
            if j == self._max:
                break

        is_valid = not (i < self._min or (
            not self._opt and i and i == j))

        if is_valid:
            root._append_tree(tree, node, pos)

        return is_valid, pos

    def _run_export_js(self, js_indent, indent, classes, cname):
        return 'List({}, {}, {}, {}, {})'.format(
            self._element._export_js(js_indent, indent, classes, cname),
            self._delimiter._export_js(js_indent, indent, classes, cname),
            self._min,
            self._max or 'undefined',
            'true' if self._opt else 'false')

    def _run_export_py(self, py_indent, indent, classes):
        return 'List({}, {}, {}, {}, {})'.format(
            self._element._export_py(py_indent, indent, classes),
            self._delimiter._export_py(py_indent, indent, classes),
            self._min,
            self._max or 'None',
            'True' if self._opt else 'False')

    @c_export
    def _run_export_c(self, c_indent, indent, enums, gid):
        return 'cleri_list({}, {}, {}, {}, {}, {})'.format(
            gid,
            self._element._export_c(c_indent, indent, enums),
            self._delimiter._export_c(c_indent, indent, enums),
            self._min,
            self._max or '0',
            '1' if self._opt else '0')

    @go_export
    def _run_export_go(self, go_indent, indent, enums, gid):
        return 'goleri.NewList({}, {}, {}, {}, {}, {})'.format(
            gid,
            self._element._export_go(go_indent, indent, enums),
            self._delimiter._export_go(go_indent, indent, enums),
            self._min,
            self._max or '0',
            'true' if self._opt else 'false')

    @java_export
    def _run_export_java(self, java_indent, indent, enums, classes, gid):
        return 'new List({}{}, {}, {}, {}, {})'.format(
            '' if gid is None else 'Ids.{}, '.format(gid),
            self._element._export_java(java_indent, indent, enums, classes),
            self._delimiter._export_java(java_indent, indent, enums, classes),
            self._min,
            self._max or 'null',
            'true' if self._opt else 'false')
