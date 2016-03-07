'''This class and THIS instance.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
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

    def _export_js(self, js_identation, ident, classes):
        classes.add('THIS')
        return 'THIS'

    def _export_c(self, c_identation, ident, enums):
        return 'CLERI_THIS'

THIS = This()
