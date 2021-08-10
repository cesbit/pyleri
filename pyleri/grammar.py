'''pyleri.Grammar Class.

When creating a new grammar this class should be used as the base class.

Example:

class MyGrammar(Grammar):
    ...


:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''


import re
import time
from .node import Node
from .expecting import Expecting
from .endofstatement import end_of_statement
from .elements import Element, NamedElement, camel_case
from .keyword import Keyword
from .ref import Ref
from .result import Result
from .exceptions import (
    KeywordError,
    ReKeywordsChangedError,
    NameAssignedError,
    MissingRefError,
    MissingStartError,
    UnusedElementError)


_RE_KEYWORDS = re.compile(r'^\w+')


class _KeepOrder(dict):

    def __init__(self, *args):
        self._order = []
        self._refs = {}
        self._re_keywords = _RE_KEYWORDS
        self._has_keywords = False
        super().__setitem__('_order', self._order)
        super().__setitem__('_refs', self._refs)

    def _check_keywords(self, element):
        if isinstance(element, Keyword):
            self._has_keywords = True
            m = self._re_keywords.match(element._keyword)
            if m is None or m.group(0) != element._keyword:
                raise KeywordError(
                    'Keyword {} does not match Grammars keywords match'
                    .format(element._keyword))
        elif hasattr(element, '_elements'):
            for elem in element._elements:
                self._check_keywords(elem)

    def __setitem__(self, key, value):
        if key not in self:
            for k in self._order:
                if k.upper() == key.upper():
                    raise NameAssignedError(
                        'Element names must be unique in a case in-sensitive '
                        'way. Cannot set both "{}" and "{}".'.format(
                            k, key))
            self._order.append(key)
        elif key in self._refs:
            self._refs[key].element = value
            if isinstance(value, NamedElement):
                value.name = key
            return

        if isinstance(value, Ref):
            self._refs[key] = value

        if key == 'RE_KEYWORDS':
            if self._has_keywords:
                raise ReKeywordsChangedError(
                    'RE_KEYWORDS must be set on top of Grammar before '
                    'keywords are set.')
            self._re_keywords = value

        if isinstance(value, NamedElement):
            if hasattr(value, 'name'):
                raise NameAssignedError(
                    'Element name is set to {0!r} and therefore cannot be '
                    'set to {1!r}. Use Repeat({0}, 1, 1) as a workaround.'
                    .format(value.name, key))
            self._check_keywords(value)
            value.name = key

        super().__setitem__(key, value)


def _used_checker(elem, used):
    if hasattr(elem, 'name') and not isinstance(elem, Ref):
        if elem.name in used:
            return
        used.add(elem.name)
    if hasattr(elem, '_element'):
        _used_checker(elem._element, used)
        if hasattr(elem, '_delimiter'):
            _used_checker(elem._delimiter, used)
    elif hasattr(elem, '_elements'):
        for el in elem._elements:
            _used_checker(el, used)


class _OrderedClass(type):

    @classmethod
    def __prepare__(mcs, name, bases):
        return _KeepOrder()

    def __new__(mcs, name, bases, attrs, **kwargs):
        for n, ref in attrs['_refs'].items():
            if ref.element is None:
                raise MissingRefError(
                    'Forward reference {!r} is createad but the '
                    'actual reference is missing.'.format(n))
        if bases and not isinstance(attrs.get('START'), Element):
            raise MissingStartError(
                'Grammar is missing the required START element entry point.')
        if bases:
            used = set()
            _used_checker(attrs['START'], used)
            elems = {
                elem for elem in attrs['_order']
                if isinstance(attrs[elem], Element)}
            if used != elems:
                raise UnusedElementError(
                    'Unused element(s) found: {}'.format(
                        ', '.join(elems - used)))

        return super().__new__(mcs, name, bases, attrs)


class Grammar(metaclass=_OrderedClass):

    __slots__ = ('_element', '_string', '_expecting', '_cached_kw_match')

    RE_KEYWORDS = _RE_KEYWORDS

    JS_INDENTATION = ' ' * 4
    JS_MODULE_NAME = 'jsleri'
    JS_WINDOW_TEMPLATE = '''
/* jshint newcap: false */

/*
 * This grammar is generated using the Grammar.export_js() method and
 * should be used with the {js_module} JavaScript module.
 *
 * Source class: {name}
 * Created at: {datetime}
 */

'use strict';

(function (
{arguments}
{indent}{indent}) {{
{language}
{refs}

{indent}window.{name} = Grammar(START, '{re_keywords}');

}})(
{constructors}
);
'''.lstrip()

    JS_ES6_IMPORT_EXPORT_TEMPLATE = '''
/*
 * This grammar is generated using the Grammar.export_js() method and
 * should be used with the `{js_module}` JavaScript module.
 *
 * Source class: {name}
 * Created at: {datetime}
 */

import {{ {classes} }} from 'jsleri';

class {name} extends Grammar {{
{language}

{indent}constructor() {{
{indent}{indent}super({name}.START, '{re_keywords}');
{indent}}}
}}
{refs}

export default {name};
'''.lstrip()

    PY_INDENTATION = ' ' * 4
    PY_MODULE_NAME = 'pyleri'
    PY_TEMPLATE = '''
"""
 This grammar is generated using the Grammar.export_py() method and
 should be used with the {py_module} python module.

 Source class: {name}
 Created at: {datetime}
"""
import re
{imports}

class {name}(Grammar):
{indent}
{indent}RE_KEYWORDS = re.compile('{re_keywords}')
{language}
'''.lstrip()

    C_INDENTATION = ' ' * 4
    C_TARGET = 'grammar'
    C_TEMPLATE_C = '''
/*
 * {target}.c
 *
 * This grammar is generated using the Grammar.export_c() method and
 * should be used with the libcleri module.
 *
 * Source class: {name}
 * Created at: {datetime}
 */

#include {header_file}
#include <stdio.h>

#define CLERI_CASE_SENSITIVE 0
#define CLERI_CASE_INSENSITIVE 1

#define CLERI_FIRST_MATCH 0
#define CLERI_MOST_GREEDY 1

cleri_grammar_t * compile_{fun}(void)
{{
{language}

    cleri_grammar_t * grammar = cleri_grammar(START, "{re_keywords}");

    return grammar;
}}
'''.lstrip()

    C_TEMPLATE_H = '''
/*
 * {target}.h
 *
 * This grammar is generated using the Grammar.export_c() method and
 * should be used with the libcleri module.
 *
 * Source class: {name}
 * Created at: {datetime}
 */
#ifndef CLERI_EXPORT_{guard}_H_
#define CLERI_EXPORT_{guard}_H_

#include <cleri/cleri.h>

cleri_grammar_t * compile_{fun}(void);

enum cleri_grammar_ids {{
    CLERI_NONE,   // used for objects with no name
{enums}
    CLERI_END // can be used to get the enum length
}};

#endif /* CLERI_EXPORT_{guard}_H_ */

'''.lstrip()

    GO_INDENTATION = '\t'
    GO_PACKAGE = 'grammar'
    GO_TEMPLATE = '''
package {package}

// This grammar is generated using the Grammar.export_go() method and
// should be used with the goleri module.
//
// Source class: {name}
// Created at: {datetime}

import (
\t"regexp"

\t"github.com/transceptor-technology/goleri"
)

// Element indentifiers
const (
\tNoGid = iota
{enums}
)

// {name} returns a compiled goleri grammar.
func {name}() *goleri.Grammar {{
{language}
{indent}return goleri.NewGrammar(START, regexp.MustCompile(`{re_keywords}`))
}}
'''.lstrip()

    JAVA_INDENTATION = '    '
    JAVA_PACKAGE = None
    JAVA_TEMPLATE = '''
{package}
/**
 * This grammar is generated using the Grammar.export_java() method and
 * should be used with the jleri module.
 *
 * Source class: {name}
 * Created at: {datetime}
 */

{imports}

{public}class {name} extends Grammar {{
{indent}enum Ids {{
{enums}
{indent}}}

{language}

{indent}{public}{name}() {{
{indent}{indent}super(START, "{re_keywords}");
{refs}{indent}}}
}}
'''.lstrip()

    def __init__(self):
        '''Initialize the grammar.

        Note: usually you should only initialize a Grammar instance
        once in a project.
        '''
        self._element = self.START
        self._string = None
        self._expecting = None
        self._cached_kw_match = {}

    def export_js(
            self,
            js_module_name=JS_MODULE_NAME,
            js_template=JS_ES6_IMPORT_EXPORT_TEMPLATE,
            js_indent=JS_INDENTATION):
        '''Export the grammar to a JavaScript file which can be
        used with the js-lrparsing module.

        Two templates are available:
            Grammar.JS_WINDOW_TEMPLATE
            Grammar.JS_ES6_IMPORT_EXPORT_TEMPLATE (default)
        '''

        language = []
        refs = []
        classes = {'Grammar'}
        indent = 0
        cname = self.__class__.__name__ if 'import ' in js_template else None

        for name in self._order:
            elem = getattr(self, name, None)
            if not isinstance(elem, Element):
                continue
            if not hasattr(elem, '_export_js'):
                continue
            language.append('{indent}{var} {name} = {value};'.format(
                indent=js_indent,
                name=name,
                var='static' if cname else 'var',
                value=elem._export_js(js_indent, indent, classes, cname)))

        for name, ref in self._refs.items():
            refs.append(
                    '{pre}{name}.set({value});'
                    .format(
                        pre='{}.'.format(cname) if cname else js_indent,
                        name=name,
                        value=ref._element._export_js(
                            js_indent,
                            -1 if cname else indent,
                            classes,
                            cname)))

        if 'Rule' in classes:
            classes.remove('Rule')

        return js_template.format(
            name=self.__class__.__name__,
            indent=js_indent,
            js_module=js_module_name,
            datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            language='\n'.join(language),
            refs='\n{}'.format('\n'.join(refs)),
            arguments=',\n'.join(map(lambda s:
                                     js_indent * 3 + s, classes)),
            re_keywords=self.RE_KEYWORDS.pattern.replace('\\', '\\\\'),
            classes=', '.join(classes),
            constructors=',\n'.join(
                map(lambda s: js_indent + s,
                    ['.'.join([
                        'window',
                        js_module_name, n]) for n in classes])))

    def export_py(
            self,
            py_module_name=PY_MODULE_NAME,
            py_template=PY_TEMPLATE,
            py_indent=PY_INDENTATION):
        '''Export the grammar to a python file which can be
        used with the pyleri module. This can be useful when python code
        if used to auto-create a grammar and an export of the final result is
        required.'''

        language = []
        classes = {'Grammar'}
        indent = 0

        for name in self._order:
            elem = getattr(self, name, None)
            if not isinstance(elem, Element):
                continue
            if not hasattr(elem, '_export_py'):
                continue
            language.append('{indent}{name} = {value}'.format(
                indent=py_indent,
                name=name,
                value=elem._export_py(py_indent, indent, classes)))

        for name, ref in self._refs.items():
            language.append(
                '{indent}{name} = {value}'
                .format(
                    indent=py_indent,
                    name=name,
                    value=ref._element._export_py(
                        py_indent,
                        indent,
                        classes)))

        return py_template.format(
            name=self.__class__.__name__,
            indent=py_indent,
            py_module=py_module_name,
            datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            language='\n'.join(language),
            re_keywords=self.RE_KEYWORDS.pattern.replace('\\', '\\\\'),
            imports='\n'.join(
                map(lambda s: s, [
                    ' '.join(['from', py_module_name, 'import', n])
                    for n in classes if n != 'Rule'])))

    def export_c(self, target=C_TARGET, c_indent=C_INDENTATION, headerf=None):
        '''Export the grammar to a c (source and header) file which can be
        used with the libcleri module.'''
        language = []
        indent = 0
        enums = set()
        for name in self._order:
            elem = getattr(self, name, None)
            if not isinstance(elem, Element):
                continue
            if not hasattr(elem, '_export_c'):
                continue
            language.append(
                '{indent}cleri_t * {name} = {value};'.format(
                    indent=c_indent,
                    name=name,
                    value=elem._export_c(c_indent, indent, enums)))

        for name, ref in self._refs.items():
            language.append(
                '{indent}cleri_ref_set({name}, {value});'
                .format(
                    indent=c_indent,
                    name=name,
                    value=ref._element._export_c(
                        c_indent,
                        indent,
                        enums,
                        ref)))

        pattern = self.RE_KEYWORDS.pattern.replace('\\', '\\\\')
        if not pattern.startswith('^'):
            pattern = '^' + pattern

        enums = ',\n'.join([
            '{}{}'.format(c_indent, gid)
            for gid in sorted(enums)]) + ','

        header_file = '"{}.h"'.format(target) if headerf is None else headerf

        fun = target.strip('/').replace('/', '_')

        return (self.__class__.C_TEMPLATE_C.format(
                    name=self.__class__.__name__,
                    target=target,
                    header_file=header_file,
                    fun=fun,
                    indent=c_indent,
                    datetime=time.strftime(
                        '%Y-%m-%d %H:%M:%S',
                        time.localtime()),
                    language='\n'.join(language),
                    re_keywords=pattern),
                self.__class__.C_TEMPLATE_H.format(
                    name=self.__class__.__name__,
                    target=target,
                    fun=fun,
                    guard=target.upper().replace('/', '_').replace('\\', '_'),
                    datetime=time.strftime(
                        '%Y-%m-%d %H:%M:%S',
                        time.localtime()),
                    language='\n'.join(language),
                    enums=enums))

    def export_go(
            self,
            go_template=GO_TEMPLATE,
            go_indent=GO_INDENTATION,
            go_package=GO_PACKAGE):
        '''Export the grammar to a Go file which can be
        used with the goleri module.'''

        language = []
        enums = set()
        indent = 0
        pattern = self.RE_KEYWORDS.pattern.replace('`', '` + "`" + `')
        if not pattern.startswith('^'):
            pattern = '^' + pattern

        for name in self._order:
            elem = getattr(self, name, None)
            if not isinstance(elem, Element):
                continue
            if not hasattr(elem, '_export_go'):
                continue
            language.append('{indent}{name} := {value}'.format(
                indent=go_indent,
                name=camel_case(name),
                value=elem._export_go(go_indent, indent, enums)))

        for name, ref in self._refs.items():
            language.append(
                    '{indent}{name}.Set({value})'
                    .format(
                        indent=go_indent,
                        name=camel_case(name),
                        value=ref._element._export_go(
                            go_indent,
                            indent,
                            enums)))

        enums = ' = iota\n'.join([
            '{}{}'.format(go_indent, gid)
            for gid in sorted(enums)]) + ' = iota'

        return go_template.format(
            name=self.__class__.__name__,
            indent=go_indent,
            package=go_package,
            datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            language='\n'.join(language),
            re_keywords=pattern,
            enums=enums)

    def export_java(
            self,
            java_template=JAVA_TEMPLATE,
            java_indent=JAVA_INDENTATION,
            java_package=JAVA_PACKAGE,
            is_public=True):
        '''Export the grammar to a Java file which can be
        used with the jleri module.'''

        language = []
        enums = set()
        classes = {'jleri.Grammar', 'jleri.Element'}

        refs = []
        indent = 0
        pattern = self.RE_KEYWORDS.pattern.replace('\\', '\\\\')
        if not pattern.startswith('^'):
            pattern = '^' + pattern

        for name in self._order:
            elem = getattr(self, name, None)
            if not isinstance(elem, Element):
                continue
            if not hasattr(elem, '_export_java'):
                continue
            language.append(
                '{indent}private static final Element {name} = {value};'
                .format(
                    indent=java_indent,
                    name=name.upper(),
                    value=elem._export_java(
                        java_indent, indent, enums, classes)))

        enum_str = ',\n'.join([
            '{indent}{indent}{gid}'.format(
                indent=java_indent,
                gid=gid)
            for gid in sorted(enums)])

        for name, ref in self._refs.items():
            refs.append(
                    '{indent}{indent}((Ref) {name}).set({value});'
                    .format(
                        indent=java_indent,
                        name=name.upper(),
                        value=ref._element._export_java(
                            java_indent,
                            -2,
                            enums,
                            classes)))
        return java_template.format(
            name=self.__class__.__name__,
            imports='\n'.join(
                map(lambda s: s, [
                    'import {};'.format(c)
                    for c in sorted(classes) if c != 'Rule'])),
            indent=java_indent,
            package='' if java_package is None
                    else 'package {};\n'.format(java_package),
            datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            language='\n'.join(language),
            re_keywords=pattern,
            refs='' if not refs else '{}\n'.format('\n'.join(refs)),
            enums=enum_str,
            public='public ' if is_public else '')

    def parse(self, string):
        '''Parse some string to the Grammar.

        Returns a nodeResult with the following attributes:
         - is_valid: True when the string is successfully parsed
                     by the Grammar.
         - pos: position in the string where parsing ended.
                (this is the end of the string when is_valid is True)
         - expecting: a list containing possible elements at position
                      'pos' in the string.
         - tree: the parse_tree containing a structured
                 result for the given string.
        '''
        self._string = string
        self._expecting = Expecting()
        self._cached_kw_match.clear()
        self._len_string = len(string)
        self._pos = None
        tree = Node(self._element, string, 0, self._len_string)
        node_res = Result(*self._walk(
            self._element,
            0,
            tree.children,
            self._element,
            True))

        # get rest if anything
        rest = self._string[node_res.pos:].lstrip()

        # set is_valid to False if we have 'rest' left.
        if node_res.is_valid and rest:
            node_res.is_valid = False

        # add end_of_statement to expecting if this is possible
        if not self._expecting.required and rest:
            self._expecting.set_mode_required(node_res.pos, True)
            self._expecting.update(end_of_statement, node_res.pos)

        node_res.expecting = self._expecting.get_expecting()

        # add expecting and correct pos to node_res if node_res is not valid
        if not node_res.is_valid:
            node_res.pos = self._expecting.pos

        node_res.tree = tree

        return node_res

    def _append_tree(self, tree, node, pos):
        if pos > self._expecting.pos:
            self._expecting.empty()
        node.end = pos
        tree.append(node)

    def _walk(self, element, pos, tree, rule, is_required):
        if self._pos != pos:
            self._s = self._string[pos:].lstrip()
            self._pos = self._len_string - len(self._s)
        node = Node(element, self._string, self._pos)
        self._expecting.set_mode_required(node.start, is_required)

        return element._get_node_result(self, tree, rule, self._s, node)


def create_grammar(elem, re_keywords=_RE_KEYWORDS):
    class _Grammar(Grammar):
        RE_KEYWORDS = _RE_KEYWORDS
        START = elem
    return _Grammar()
