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
from .noderesult import NodeResult
from .exceptions import (
    KeywordError,
    ReKeywordsChangedError,
    NameAssignedError)


_RE_KEYWORDS = re.compile('^\w+')


class _KeepOrder(dict):

    def __init__(self, *args):
        super().__setitem__('_order', [])
        self._RE_KEYWORDS = _RE_KEYWORDS
        self._has_keywords = False

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
            super().__getitem__('_order').append(key)

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
    def __prepare__(mcl, name, bases):
        return _KeepOrder()


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

        return js_template.format(
            name=self.__class__.__name__,
            ident=js_identation,
            js_module=js_module_name,
            datetime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            language='\n'.join(language),
            arguments=',\n'.join(map(lambda s:
                                     js_identation * 3 + s, classes)),
            re_keywords=self.RE_KEYWORDS.pattern,
            constructors=',\n'.join(
                map(lambda s: js_identation + s,
                    ['.'.join(
                        [
                            'window',
                            js_module_name, n]) for n in classes])))

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
