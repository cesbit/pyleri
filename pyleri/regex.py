'''Regex class.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
import re
from .elements import NamedElement, c_export, go_export, java_export


class Regex(NamedElement):

    __slots__ = ('_compiled',)

    def __init__(self, pattern, flags=0):
        if not pattern.startswith('^'):
            pattern = '^' + pattern
        assert flags == 0 or flags == re.IGNORECASE, \
            'Only re.IGNORECASE is currently accepted as flag'
        self._compiled = re.compile(pattern, flags=flags)

    def __repr__(self):
        name = getattr(self, 'name', None)
        return self.__class__.__name__ if name is None else '"{}"'.format(name)

    def _get_node_result(self, root, tree, rule, s, node):
        re_match = self._compiled.match(s)
        is_valid = bool(re_match)

        if is_valid:
            root._append_tree(tree, node, node.start + len(re_match.group(0)))
        else:
            root._expecting.update(self, node.start)

        return is_valid, node.end or node.start

    def _run_export_js(self, js_indent, indent, classes, cname):
        return 'Regex(\'{}\'{})'.format(
            self._compiled.pattern.replace('\\', '\\\\').replace('\'', '\\\''),
            ', true' if self._compiled.flags & re.IGNORECASE else '')

    def _run_export_py(self, py_indent, indent, classes):
        return 'Regex(\'{}\'{})'.format(
            self._compiled.pattern.replace('\\', '\\\\').replace('\'', '\\\''),
            ', re.IGNORECASE' if self._compiled.flags & re.IGNORECASE else '')

    @c_export
    def _run_export_c(self, c_indent, indent, enums, gid):
        assert not(self._compiled.flags & re.IGNORECASE), \
            'libcleri has currently no support for the re.IGNORECASE flag'
        return 'cleri_regex({}, "{}")'.format(
            gid,
            self._compiled.pattern
                .replace('\\', '\\\\')
                .replace('\'', '\\\'')
                .replace('\\"', '"')
                .replace('"', '\\"'))

    @go_export
    def _run_export_go(self, go_indent, indent, enums, gid):
        pattern = self._compiled.pattern.replace('`', '` + "`" + `')
        if self._compiled.flags & re.IGNORECASE:
            pattern = '(?i)' + pattern
        return 'goleri.NewRegex({}, regexp.MustCompile(`{}`))'.format(
            gid,
            pattern)

    @java_export
    def _run_export_java(self, java_indent, indent, enums, classes, gid):
        if self._compiled.flags & re.IGNORECASE:
            classes.add('java.util.regex.Pattern')
            return 'new Regex({}Pattern.compile("{}", {}))'.format(
                '' if gid is None else 'Ids.{}, '.format(gid),
                self._compiled.pattern
                    .replace('\\', '\\\\')
                    .replace('\'', '\\\'')
                    .replace('\\"', '"')
                    .replace('"', '\\"'),
                'Pattern.CASE_INSENSITIVE')

        return 'new Regex({}"{}")'.format(
            '' if gid is None else 'Ids.{}, '.format(gid),
            self._compiled.pattern
                .replace('\\', '\\\\')
                .replace('\'', '\\\'')
                .replace('\\"', '"')
                .replace('"', '\\"'))
