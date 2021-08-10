'''Optional class.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import NamedElement, c_export, go_export, java_export


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

    def _run_export_js(self, js_indent, indent, classes, cname):
        return 'Optional({})'.format(
            self._element._export_js(js_indent, indent, classes, cname))

    def _run_export_py(self, py_indent, indent, classes):
        return 'Optional({})'.format(
            self._element._export_py(py_indent, indent, classes))

    @c_export
    def _run_export_c(self, c_indent, indent, enums, gid):
        return 'cleri_optional({}, {})'.format(
            gid,
            self._element._export_c(c_indent, indent, enums))

    @go_export
    def _run_export_go(self, go_indent, indent, enums, gid):
        return 'goleri.NewOptional({}, {})'.format(
            gid,
            self._element._export_go(go_indent, indent, enums))

    @java_export
    def _run_export_java(self, java_indent, indent, enums, classes, gid):
        return 'new Optional({}{})'.format(
            '' if gid is None else 'Ids.{}, '.format(gid),
            self._element._export_java(java_indent, indent, enums, classes))
