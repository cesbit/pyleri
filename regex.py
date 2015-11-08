import re
from .noderesult import NodeResult
from .elements import NamedElement


class Regex(NamedElement):

    __slots__ = ('_compiled',)

    def __init__(self, pattern, flags=0):
        if not pattern.startswith('^'):
            pattern = '^' + pattern
        self._compiled = re.compile(pattern, flags=flags)

    def __repr__(self):
        if hasattr(self, 'name'):
            return '"{}"'.format(self.name)
        else:
            return self.__class__.__name__

    def _get_node_result(self, root, tree, rule, s, node):
        re_match = self._compiled.match(s)
        is_valid = bool(re_match)

        if is_valid:
            root._append_tree(tree, node, node.start + len(re_match.group(0)))
        else:
            root._expecting.update(self, node.start)

        return NodeResult(is_valid, node.end or node.start)

    def _new_export_js(self, js_identation, ident, classes):
        return 'Regex(\'{}\')'.format(
            self._compiled.pattern.replace('\\', '\\\\').replace('\'', '\\\''))
