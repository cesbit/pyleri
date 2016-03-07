'''pyleri.Choice Class.

Choose one of the given elements. When most_greedy is True we will choose
the 'longest' element when multiple elements are valid. If most_greedy is
False we will return the first match.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''

from .elements import NamedElement, c_export


class Choice(NamedElement):

    __slots__ = ('_elements', '_get_node_result')

    def __init__(self, *elements, most_greedy=True):
        self._elements = self._validate_elements(elements)
        self._get_node_result = \
            self._most_greedy_result if most_greedy else \
            self._stop_at_first_match

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

    def _run_export_js(self, js_identation, ident, classes):
        return self._export_js_elements(js_identation, ident, classes)

    @c_export
    def _run_export_c(self, c_identation, ident, enums, gid):
        new_ident = ident + 1
        value = ',\n'.join(['{ident}{elem}'.format(
            ident=c_identation * new_ident,
            elem=elem._export_c(
                c_identation,
                new_ident,
                enums)) for elem in self._elements])
        return 'cleri_choice(\n{gid},\n{mg},\n{num},\n{val}\n{ident})'.format(
            gid='{ident}{gid}'.format(
                ident=c_identation * (ident + 1),
                gid=gid),
            mg='{ident}{mg}'.format(
                ident=c_identation * (ident + 1),
                mg=('CLERI_FIRST_MATCH', 'CLERI_MOST_GREEDY')[
                    self._get_node_result == self._most_greedy_result]),
            num='{ident}{num}'.format(
                ident=c_identation * (ident + 1),
                num=len(self._elements)),
            val=value,
            ident=c_identation * ident)
