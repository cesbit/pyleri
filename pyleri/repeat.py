'''Repeat class.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import NamedElement, c_export, go_export, java_export


class Repeat(NamedElement):

    __slots__ = ('_element', '_min', '_max')

    def __init__(self, element, mi=0, ma=None):
        self._element = self._validate_element(element)

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

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def _elements(self):
        yield self._element

    def _get_node_result(self, root, tree, rule, s, node):
        pos, i = node.start, 0
        while not self._max or i < self._max:
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

        is_valid = i >= self._min
        if is_valid:
            root._append_tree(tree, node, pos)

        return is_valid, pos

    def _run_export_js(self, js_indent, indent, classes, cname):
        return 'Repeat({}, {}, {})'.format(
            self._element._export_js(js_indent, indent, classes, cname),
            self._min,
            self._max or 'undefined')

    def _run_export_py(self, py_indent, indent, classes):
        return 'Repeat({}, {}, {})'.format(
            self._element._export_py(py_indent, indent, classes),
            self._min,
            self._max or 'None')

    @c_export
    def _run_export_c(self, c_indent, indent, enums, gid):
        # If the repeat is used as a duplication we can use the duplication
        # which is supported by libcleri
        if hasattr(self._element, 'name') \
                and self._min == 1 \
                and self._max == 1:
            return 'cleri_dup({}, {})'.format(
                gid,
                self._element.name)
        return 'cleri_repeat({}, {}, {}, {})'.format(
            gid,
            self._element._export_c(c_indent, indent, enums),
            self._min,
            self._max or 0)

    @go_export
    def _run_export_go(self, go_indent, indent, enums, gid):
        return 'goleri.NewRepeat({}, {}, {}, {})'.format(
            gid,
            self._element._export_go(go_indent, indent, enums),
            self._min,
            self._max or '0')

    @java_export
    def _run_export_java(self, java_indent, indent, enums, classes, gid):
        return 'new Repeat({}{}, {}, {})'.format(
            '' if gid is None else 'Ids.{}, '.format(gid),
            self._element._export_java(java_indent, indent, enums, classes),
            self._min,
            self._max or 'null')
