'''pyleri.Grammar Class.

When creating a new grammar this class should be used as the base class.

Example:

class MyGrammar(Grammar):
    ...


:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''


import re
import time
from .node import Node
from .expecting import Expecting
from .endofstatement import end_of_statement
from .elements import Element, NamedElement
from .keyword import Keyword
from .ref import Ref
from .noderesult import NodeResult
from .exceptions import (
    KeywordError,
    ReKeywordsChangedError,
    NameAssignedError,
    MissingRefError)


_RE_KEYWORDS = re.compile('^\w+')


class _KeepOrder(dict):

    def __init__(self, *args):
        self._order = []
        self._refs = {}
        self._RE_KEYWORDS = _RE_KEYWORDS
        self._has_keywords = False
        super().__setitem__('_order', self._order)
        super().__setitem__('_refs', self._refs)

    def _check_keywords(self, element):
        if isinstance(element, Keyword):
            self._has_keywords = True
            m = self._RE_KEYWORDS.match(element._keyword)
            if m is None or m.group(0) != element._keyword:
                raise KeywordError(
                    'Keyword {} does not match Grammars keywords match'
                    .format(element._keyword))
        elif hasattr(element, '_elements'):
            for elem in element._elements:
                self._check_keywords(elem)

    def __setitem__(self, key, value):
        if key not in self:
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
            self._RE_KEYWORDS = value

        if isinstance(value, NamedElement):
            if hasattr(value, 'name'):
                raise NameAssignedError(
                    'Element name is set to {0!r} and therefore cannot be '
                    'set to {1!r}. Use Repeat({0}, 1, 1) as a workaround.'
                    .format(value.name, key))
            self._check_keywords(value)
            value.name = key

        super().__setitem__(key, value)


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
        return super().__new__(mcs, name, bases, attrs)


class Grammar(metaclass=_OrderedClass):

    __slots__ = ('_element', '_string', '_expecting', '_cached_kw_match')

    RE_LEFT_WHITESPACE = re.compile('^\s+')
    RE_KEYWORDS = _RE_KEYWORDS
    RE_WHITESPACE = re.compile('\s+')

    JS_IDENTATION = ' ' * 4
    JS_MODULE_NAME = 'jsleri'
    JS_TEMPLATE = '''
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
{ident}{ident}) {{
{language}

{ident}window.{name} = Grammar(START, '{re_keywords}');

}})(
{constructors}
);
'''.lstrip()

    C_IDENTATION = ' ' * 4
    C_TARGET = 'grammar'
    C_TEMPLATE_C = '''
/*
 * This grammar is generated using the Grammar.export_c() method and
 * should be used with the cleri module.
 *
 * Source class: {name}
 * Created at: {datetime}
 */

#include <{target}.h>
#include <stdio.h>

#define CLERI_CASE_SENSITIVE 0
#define CLERI_CASE_INSENSITIVE 1

#define CLERI_FIRST_MATCH 0
#define CLERI_MOST_GREEDY 1

cleri_grammar_t * compile_grammar(void)
{{
{language}

    cleri_grammar_t * grammar = cleri_grammar(START, "{re_keywords}");

    return grammar;
}}
'''.lstrip()

    C_TEMPLATE_H = '''
/*
 * This grammar is generated using the Grammar.export_c() method and
 * should be used with the cleri module.
 *
 * Source class: {name}
 * Created at: {datetime}
 */

#pragma once

#include <{target}.h>
#include <cleri/object.h>

cleri_grammar_t * compile_grammar(void);

enum cleri_grammar_ids {{
    CLERI_NONE,   // used for objects with no name
{enums}
    CLERI_END // can be used to get the enum length
}};

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
            js_template=JS_TEMPLATE,
            js_identation=JS_IDENTATION):
        '''Export the grammar as a JavaScript file which can be
        used with the js-lrparsing module.'''

        language = []
        classes = {'Grammar'}
        ident = 0

        for name in self._order:
            elem = getattr(self, name, None)
            if not isinstance(elem, Element):
                continue
            if not hasattr(elem, '_export_js'):
                continue
            language.append('{ident}var {name} = {value};'.format(
                ident=js_identation,
                name=name,
                value=elem._export_js(js_identation, ident, classes)))

        for name, ref in self._refs.items():
            language.append('{ident}Object.assign({name}, {value});'
                .format(
                    ident=js_identation,
                    name=name,
                    value=ref._element._export_js(
                        js_identation,
                        ident,
                        classes)))


        return js_template.format(
            name=self.__class__.__name__,
            ident=js_identation,
            js_module=js_module_name,
            datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            language='\n'.join(language),
            arguments=',\n'.join(map(lambda s:
                                     js_identation * 3 + s, classes)),
            re_keywords=self.RE_KEYWORDS.pattern.replace('\\', '\\\\'),
            constructors=',\n'.join(
                map(lambda s: js_identation + s,
                    ['.'.join(
                        [
                            'window',
                            js_module_name, n]) for n in classes])))

    def export_c(self, target=C_TARGET, c_identation=C_IDENTATION):
        language = []
        ident = 0
        enums = set()
        for name in self._order:
            elem = getattr(self, name, None)
            if not isinstance(elem, Element):
                continue
            if not hasattr(elem, '_export_c'):
                continue
            if isinstance(elem, Ref):
                language.append(
                    '{ident}cleri_object_t * {name};'.format(
                        ident=c_identation,
                        name=name))
            else:
                language.append(
                    '{ident}cleri_object_t * {name} = {value};'.format(
                        ident=c_identation,
                        name=name,
                        value=elem._export_c(c_identation, ident, enums)))

        for name, ref in self._refs.items():
            language.append('{ident}{name} = {value};'
                .format(
                    ident=c_identation,
                    name=name,
                    value=ref._element._export_c(
                        c_identation,
                        ident,
                        enums)))

        pattern = self.RE_KEYWORDS.pattern.replace('\\', '\\\\')
        if not pattern.startswith('^'):
            pattern = '^' + pattern

        enums = ',\n'.join([
            '{}{}'.format(c_identation, gid)
            for gid in sorted(enums)]) + ','

        return (self.__class__.C_TEMPLATE_C.format(
                    name=self.__class__.__name__,
                    target=target,
                    ident=c_identation,
                    datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                    language='\n'.join(language),
                    re_keywords=pattern),
                self.__class__.C_TEMPLATE_H.format(
                    name=self.__class__.__name__,
                    target=target,
                    datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                    language='\n'.join(language),
                    enums=enums))

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
        node_res = NodeResult(*self._walk(
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
