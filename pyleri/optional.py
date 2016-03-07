'''Optional class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .elements import NamedElement, c_export


class Optional(NamedElement):

    __slots__ = ('_element',)

    def __init__(self, element):
        self._element = self._validate_element(element)

    @property
    def _elements(self):
        yield self._element

    def _get_node_result(self, root, tree, rule, _s, node):
        is_valid, pos = root._walk(
            self._element,
            node.start,
            node.children,
            rule,
            False)
        if is_valid:
            root._append_tree(tree, node, pos)

        return True, node.end or node.start

    def _run_export_js(self, js_identation, ident, classes):
        return 'Optional({})'.format(
            self._element._export_js(js_identation, ident, classes))

    @c_export
    def _run_export_c(self, c_identation, ident, enums, gid):
        return 'cleri_optional({}, {})'.format(
            gid,
            self._element._export_c(c_identation, ident, enums))