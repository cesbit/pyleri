'''Sequence class.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import NamedElement, c_export


class Sequence(NamedElement):

    __slots__ = ('_elements',)

    def __init__(self, *elements):
        self._elements = self._validate_elements(elements)

    def _get_node_result(self, root, tree, rule, _s, node):
        pos = node.start

        for elem in self._elements:
            is_valid, pos = root._walk(elem, pos, node.children, rule, True)
            if not is_valid:
                return is_valid, pos

        root._append_tree(tree, node, pos)

        return is_valid, pos

    def _run_export_js(self, js_indent, indent, classes, cname):
        return self._export_js_elements(js_indent, indent, classes, cname)

    def _run_export_py(self, py_indent, indent, classes):
        return self._export_py_elements(py_indent, indent, classes)

    def _run_export_c(self, c_indent, indent, enums):
        return self._export_c_elements(c_indent, indent, enums)

    def _run_export_go(self, go_indent, indent, enums):
        return self._export_go_elements(go_indent, indent, enums)

    def _run_export_java(self, java_indent, indent, enums, classes):
        return self._export_java_elements(java_indent, indent, enums, classes)
