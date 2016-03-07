'''Repeat class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement, c_export


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

    def _run_export_js(self, js_identation, ident, classes):
        return 'Repeat({}, {}, {})'.format(
            self._element._export_js(js_identation, ident, classes),
            self._min,
            self._max or 'undefined')

    @c_export
    def _run_export_c(self, c_identation, ident, enums, gid):
        return 'cleri_repeat({}, {}, {}, {})'.format(
            gid,
            self._element._export_c(c_identation, ident, enums),
            self._min,
            self._max or 'undefined')