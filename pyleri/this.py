'''This class and THIS instance.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import Element


class This(Element):

    def _get_node_result(self, root, tree, rule, _s, node):
        if node.start not in rule._tested:
            rule._tested[node.start] = root._walk(
                rule._element,
                node.start,
                node.children,
                rule,
                True)
            rule._tree[node.start] = node.children

        if rule._tested[node.start][0]:
            node.children = rule._tree[node.start]
            root._append_tree(tree, node, rule._tested[node.start][1])

        return rule._tested[node.start]

    def _export_js(self, js_indent, indent, classes, cname):
        classes.add('THIS')
        return 'THIS'

    def _export_py(self, py_indent, indent, classes):
        classes.add('THIS')
        return 'THIS'

    def _export_c(self, c_indent, indent, enums):
        return 'CLERI_THIS'

    def _export_go(self, go_indent, indent, enums):
        return 'goleri.THIS'

    def _export_java(self, java_indent, indent, enums, classes):
        classes.add('jleri.This')
        return 'This.THIS'


THIS = This()
