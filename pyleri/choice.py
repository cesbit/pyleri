'''pyleri.Choice Class.

Choose one of the given elements. When most_greedy is True we will choose
the 'longest' element when multiple elements are valid. If most_greedy is
False we will return the first match.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''

from .elements import NamedElement, c_export, go_export, java_export


class Choice(NamedElement):

    __slots__ = ('_elements', '_get_node_result')

    def __init__(self, *elements, most_greedy=True):
        self._elements = self._validate_elements(elements)
        self._get_node_result = \
            self._most_greedy_result if most_greedy else \
            self._stop_at_first_match

    @property
    def most_greedy(self):
        return self._get_node_result == self._most_greedy_result

    def _most_greedy_result(self, root, tree, rule, s, node):
        mg_is_valid, mg_pos = False, node.start

        for elem in self._elements:
            children = []
            is_valid, pos = root._walk(elem, node.start, children, rule, True)

            if is_valid and pos > mg_pos:
                node.children = children
                mg_is_valid, mg_pos = is_valid, pos

        if mg_is_valid:
            root._append_tree(tree, node, mg_pos)

        return mg_is_valid, mg_pos

    def _stop_at_first_match(self, root, tree, rule, s, node):
        for elem in self._elements:
            children = []
            is_valid, pos = root._walk(elem, node.start, children, rule, True)

            if is_valid:
                node.children = children
                root._append_tree(tree, node, pos)
                break

        return is_valid, pos

    def _run_export_js(self, js_indent, indent, classes, cname):
        return self._export_js_elements(js_indent, indent, classes, cname)

    def _run_export_py(self, py_indent, indent, classes):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=py_indent * new_indent,
            elem=elem._export_py(
                py_indent,
                new_indent,
                classes)) for elem in self._elements])
        return 'Choice(\n{val},\n{indent}most_greedy={mg})'.format(
            mg='{mg}'.format(
                indent=py_indent * (indent + 1),
                mg=('False', 'True')[
                    self._get_node_result == self._most_greedy_result]),
            val=value,
            indent=py_indent * new_indent)

    @c_export
    def _run_export_c(self, c_indent, indent, enums, gid):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=c_indent * new_indent,
            elem=elem._export_c(
                c_indent,
                new_indent,
                enums)) for elem in self._elements])
        return 'cleri_choice(\n{gid},\n{mg},\n{num},\n{val}\n{indent})'.format(
            gid='{indent}{gid}'.format(
                indent=c_indent * (indent + 1),
                gid=gid),
            mg='{indent}{mg}'.format(
                indent=c_indent * (indent + 1),
                mg=('CLERI_FIRST_MATCH', 'CLERI_MOST_GREEDY')[
                    self._get_node_result == self._most_greedy_result]),
            num='{indent}{num}'.format(
                indent=c_indent * (indent + 1),
                num=len(self._elements)),
            val=value,
            indent=c_indent * indent)

    @go_export
    def _run_export_go(self, go_indent, indent, enums, gid):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=go_indent * new_indent,
            elem=elem._export_go(
                go_indent,
                new_indent,
                enums)) for elem in self._elements])
        return 'goleri.NewChoice(\n{gid},\n{mg},\n{val},\n{indent})'.format(
            gid='{indent}{gid}'.format(
                indent=go_indent * (indent + 1),
                gid=gid),
            mg='{indent}{mg}'.format(
                indent=go_indent * (indent + 1),
                mg=('false', 'true')[
                    self._get_node_result == self._most_greedy_result]),
            val=value,
            indent=go_indent * indent)

    @java_export
    def _run_export_java(self, java_indent, indent, enums, classes, gid):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=java_indent * new_indent,
            elem=elem._export_java(
                java_indent,
                new_indent,
                enums,
                classes)) for elem in self._elements])
        return 'new Choice({gid}\n{mg},\n{val}\n{indent})'.format(
            gid='' if gid is None else '\n{indent}Ids.{gid},'.format(
                indent=java_indent * (indent + 1),
                gid=gid),
            mg='{indent}{mg}'.format(
                indent=java_indent * (indent + 1),
                mg=('false', 'true')[
                    self._get_node_result == self._most_greedy_result]),
            val=value,
            indent=java_indent * indent)
