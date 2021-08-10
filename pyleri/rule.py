'''Rule class.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import NamedElement


class Rule(NamedElement):

    __slots__ = ('_element', '_tested', '_tree', '_depth')

    def __init__(self, element):
        self._element = element

    def _get_node_result(self, root, tree, rule, _s, node):
        self._tested = {}
        self._tree = {}
        self._depth = -1
        is_valid, pos = root._walk(
            self._element,
            node.start,
            node.children,
            self,
            True)
        if is_valid:
            root._append_tree(tree, node, pos)
        return is_valid, pos

    def _run_export_js(self, js_indent, indent, classes, cname):
        return self._element._export_js(js_indent, indent, classes, cname)

    def _run_export_py(self, py_indent, indent, classes):
        return self._element._export_py(py_indent, indent, classes)

    def _run_export_c(self, c_indent, indent, enums):
        name = getattr(self, 'name', None)
        if name is not None:
            self._element._name = name
        return self._element._export_c(c_indent, indent, enums)

    def _run_export_go(self, go_indent, indent, enums):
        name = getattr(self, 'name', None)
        if name is not None:
            self._element._name = name
        return self._element._export_go(go_indent, indent, enums)

    def _run_export_java(self, java_indent, indent, enums, classes):
        name = getattr(self, 'name', None)
        if name is not None:
            self._element._name = name
        return self._element._export_java(java_indent, indent, enums, classes)
