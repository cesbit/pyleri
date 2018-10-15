Python Left-Right Parser
========================
Pyleri is an easy-to-use parser created for [SiriDB](http://siridb.net/). We first used [lrparsing](http://lrparsing.sourceforge.net/doc/html/) and wrote [jsleri](https://github.com/transceptor-technology/jsleri) for auto-completion and suggestions in our web console. Later we found small issues within the `lrparsing` module and also had difficulties keeping the language the same in all projects. That is when we decided to create Pyleri which can export a created grammar to JavaScript, C, Python, Go and Java.

---------------------------------------
  * [Related projects](#related-projects)
  * [Installation](#installation)
  * [Quick usage](#quick-usage)
  * [Grammar](#grammar)
    * [Grammar.parse()](#parse)
    * [Grammar.export_js()](#export_js)
    * [Grammar.export_c()](#export_c)
    * [Grammar.export_go()](#export_go)
    * [Grammar.export_java()](#export_java)
    * [Grammar.export_py()](#export_py)
  * [Result](#result)
    * [is_valid](#is_valid)
    * [Position](#position)
    * [Tree](#tree)
    * [Expecting](#expecting)
  * [Elements](#elements)
    * [Keyword](#keyword)
    * [Regex](#regex)
    * [Token](#token)
    * [Tokens](#tokens)
    * [Sequence](#sequence)
    * [Choice](#choice)
    * [Repeat](#repeat)
    * [List](#list)
    * [Optional](#optional)
    * [Ref](#ref)
    * [Prio](#prio)


---------------------------------------
## Related projects
- [jsleri](https://github.com/transceptor-technology/jsleri): JavaScript parser
- [libcleri](https://github.com/transceptor-technology/libcleri): C parser
- [goleri](https://github.com/transceptor-technology/goleri): Go parser
- [jleri](https://github.com/transceptor-technology/jleri): Java parser

## Installation
The easiest way is to use PyPI:

    sudo pip3 install pyleri

## Quick usage
```python
# Imports, note that we skip the imports in other examples...
from pyleri import (
    Grammar,
    Keyword,
    Regex,
    Sequence)

# Create a Grammar Class to define your language
class MyGrammar(Grammar):
    r_name = Regex('(?:"(?:[^"]*)")+')
    k_hi = Keyword('hi')
    START = Sequence(k_hi, r_name)

# Compile your grammar by creating an instance of the Grammar Class.
my_grammar = MyGrammar()

# Use the compiled grammar to parse 'strings'
print(my_grammar.parse('hi "Iris"').is_valid) # => True
print(my_grammar.parse('bye "Iris"').is_valid) # => False
print(my_grammar.parse('bye "Iris"').as_str()) # => error at position 0, expecting: hi
```

## Grammar
When writing a grammar you should subclass Grammar. A Grammar expects at least a `START` property so the parser knows where to start parsing. Grammar has some default properties which can be overwritten like `RE_KEYWORDS`, which will be explained later. Grammar also has a parse method: `parse()`, and a few export methods: [export_js()](#export_js), [export_c()](#export_c), [export_py()](#export_py), [export_go()](#export_go) and [export_java()](#export_java) which are explained below.


### parse
syntax:
```python
Grammar().parse(string)
```
The `parse()` method returns a result object which has the following properties that are further explained in [Result](#result):
- `expecting`
- `is_valid`
- `pos`
- `tree`


### export_js
syntax:
```python
Grammar().export_js(
    js_module_name='jsleri',
    js_template=Grammar.JS_TEMPLATE,
    js_indent=' ' * 4)
```
Optional keyword arguments:
- `js_module_name`: Name of the JavaScript module. (default: 'jsleri')
- `js_template`: Template String used for the export. You might want to look at the default string which can be found at Grammar.JS_TEMPLATE.
- `js_indent`: indentation used in the JavaScript file. (default: 4 spaces)

For example when using our Quick usage grammar, this is the output when running `my_grammar.export_js()`:
```javascript
/* jshint newcap: false */

/*
 * This grammar is generated using the Grammar.export_js() method and
 * should be used with the jsleri JavaScript module.
 *
 * Source class: MyGrammar
 * Created at: 2015-11-04 10:06:06
 */

'use strict';

(function (
            Regex,
            Sequence,
            Keyword,
            Grammar
        ) {
    var r_name = Regex('^(?:"(?:[^"]*)")+');
    var k_hi = Keyword('hi');
    var START = Sequence(
        k_hi,
        r_name
    );

    window.MyGrammar = Grammar(START, '^\w+');

})(
    window.jsleri.Regex,
    window.jsleri.Sequence,
    window.jsleri.Keyword,
    window.jsleri.Grammar
);
```

### export_c
syntax:
```python
Grammar().export_c(
    target=Grammar.C_TARGET,
    c_indent=' ' * 4)
```
Optional keyword arguments:
- `target`: Name of the c module. (default: 'grammar')
- `c_indent`: indentation used in the c files. (default: 4 spaces)

The return value is a tuple containing the source (c) file and header (h) file.

For example when using our Quick usage grammar, this is the output when running `my_grammar.export_c()`:
```c
/*
 * grammar.c
 *
 * This grammar is generated using the Grammar.export_c() method and
 * should be used with the libcleri module.
 *
 * Source class: MyGrammar
 * Created at: 2016-05-09 12:16:49
 */

#include "grammar.h"
#include <stdio.h>

#define CLERI_CASE_SENSITIVE 0
#define CLERI_CASE_INSENSITIVE 1

#define CLERI_FIRST_MATCH 0
#define CLERI_MOST_GREEDY 1

cleri_grammar_t * compile_grammar(void)
{
    cleri_t * r_name = cleri_regex(CLERI_GID_R_NAME, "^(?:\"(?:[^\"]*)\")+");
    cleri_t * k_hi = cleri_keyword(CLERI_GID_K_HI, "hi", CLERI_CASE_INSENSITIVE);
    cleri_t * START = cleri_sequence(
        CLERI_GID_START,
        2,
        k_hi,
        r_name
    );

    cleri_grammar_t * grammar = cleri_grammar(START, "^\\w+");

    return grammar;
}
```
and the header file...
```c
/*
 * grammar.h
 *
 * This grammar is generated using the Grammar.export_c() method and
 * should be used with the libcleri module.
 *
 * Source class: MyGrammar
 * Created at: 2016-05-09 12:16:49
 */
#ifndef CLERI_EXPORT_GRAMMAR_H_
#define CLERI_EXPORT_GRAMMAR_H_

#include <grammar.h>
#include <cleri/cleri.h>

cleri_grammar_t * compile_grammar(void);

enum cleri_grammar_ids {
    CLERI_NONE,   // used for objects with no name
    CLERI_GID_K_HI,
    CLERI_GID_R_NAME,
    CLERI_GID_START,
    CLERI_END // can be used to get the enum length
};

#endif /* CLERI_EXPORT_GRAMMAR_H_ */

```
### export_go
syntax:
```python
Grammar().export_go(
    go_template=Grammar.GO_TEMPLATE,
    go_indent='\t',
    go_package='grammar')
```
Optional keyword arguments:
- `go_template`: Template String used for the export. You might want to look at the default string which can be found at Grammar.GO_TEMPLATE.
- `go_indent`: indentation used in the Go file. (default: one tab)
- `go_package`: Name of the go package. (default: 'grammar')

For example when using our Quick usage grammar, this is the output when running `my_grammar.export_go()`:
```go
package grammar

// This grammar is generated using the Grammar.export_go() method and
// should be used with the goleri module.
//
// Source class: MyGrammar
// Created at: 2017-03-14 19:07:09

import (
        "regexp"

        "github.com/transceptor-technology/goleri"
)

// Element indentifiers
const (
        NoGid = iota
        GidKHi = iota
        GidRName = iota
        GidSTART = iota
)

// MyGrammar returns a compiled goleri grammar.
func MyGrammar() *goleri.Grammar {
        rName := goleri.NewRegex(GidRName, regexp.MustCompile(`^(?:"(?:[^"]*)")+`))
        kHi := goleri.NewKeyword(GidKHi, "hi", false)
        START := goleri.NewSequence(
                GidSTART,
                kHi,
                rName,
        )
        return goleri.NewGrammar(START, regexp.MustCompile(`^\w+`))
}
```
### export_java
syntax:
```python
Grammar().export_java(
    java_template=Grammar.JAVA_TEMPLATE,
    java_indent=' ' * 4,
    java_package=None,
    is_public=True)
```
Optional keyword arguments:
- `java_template`: Template String used for the export. You might want to look at the default string which can be found at Grammar.JAVA_TEMPLATE.
- `java_indent`: indentation used in the Java file. (default: four spaces)
- `java_package`: Name of the Java package or None when no package is specified. (default: None)
- `is_public`: Class and constructor are defined as public when True, else they will be defined as package private.

For example when using our Quick usage grammar, this is the output when running `my_grammar.export_java()`:
```java
/**
 * This grammar is generated using the Grammar.export_java() method and
 * should be used with the jleri module.
 *
 * Source class: MyGrammar
 * Created at: 2018-07-04 12:12:34
 */

import jleri.Grammar;
import jleri.Element;
import jleri.Sequence;
import jleri.Regex;
import jleri.Keyword;

public class MyGrammar extends Grammar {
    enum Ids {
        K_HI,
        R_NAME,
        START
    }

    private static final Element R_NAME = new Regex(Ids.R_NAME, "^(?:\"(?:[^\"]*)\")+");
    private static final Element K_HI = new Keyword(Ids.K_HI, "hi", false);
    private static final Element START = new Sequence(
        Ids.START,
        K_HI,
        R_NAME
    );

    public MyGrammar() {
        super(START, "^\\w+");
    }
}
```
### export_py
syntax:
```python
Grammar().export_py(
    py_module_name='pyleri',
    py_template=Grammar.PY_TEMPLATE,
    py_indent=' ' * 4)
```
Optional keyword arguments:
- `py_module_name`: Name of the Pyleri Module. (default: 'pyleri')
- `py_template`: Template String used for the export. You might want to look at the default string which can be found at Grammar.PY_TEMPLATE.
- `py_indent`: indentation used in the Python file. (default: 4 spaces)

For example when using our Quick usage grammar, this is the output when running `my_grammar.export_py()`:
```python
"""
 This grammar is generated using the Grammar.export_py() method and
 should be used with the pyleri python module.

 Source class: MyGrammar
 Created at: 2017-03-14 19:14:51
"""
import re
from pyleri import Sequence
from pyleri import Keyword
from pyleri import Grammar
from pyleri import Regex

class MyGrammar(Grammar):

    RE_KEYWORDS = re.compile('^\\w+')
    r_name = Regex('^(?:"(?:[^"]*)")+')
    k_hi = Keyword('hi')
    START = Sequence(
        k_hi,
        r_name
    )
```

## Result
The result of the `parse()` method contains 4 properties that will be explained next. A function `as_str(translate=None)` is also available which will
show the result as a string. The `translate` argument should be a function which accepts an element as argument. This function can be used to
return custom strings for certain elements. If the return value of `translate` is `None` then the function will fall try to generate a string value. If
the return value is an empty string, the value will be ignored.

Example of translate functions:
```python
# In case a translation function returns an empty string, no text is used
def translate(elem):
    return ''  # as a result you get something like: 'error at position x'

# Text may be returned based on gid
def translate(elem):
    if elem is some_elem:
        return 'A'   # something like: error at position x, expecting: A
    elif elem is other_elem:
        return ''    # other_elem will be ignored
    else:
        return None  # normal parsing

# A translate function can be used as follow:
print(my_grammar.parse('some string').as_str(translate=translate))
```

### is_valid
`is_valid` returns a boolean value, `True` when the given string is valid according to the given grammar, `False` when not valid.

Let us take the example from Quick usage.
```python
res = my_grammar.parse('bye "Iris"')
print(res.is_valid) # => False
```

### Position
`pos` returns the position where the parser had to stop. (when `is_valid` is `True` this value will be equal to the length of the given string with `str.rstrip()` applied)

Let us take the example from Quick usage.
```python
result = my_grammar.parse('hi Iris')
print(res.is_valid, result.pos) # => False, 3
```

### Tree
`tree` contains the parse tree. Even when `is_valid` is `False` the parse tree is returned but will only contain results as far as parsing has succeeded. The tree is the root node which can include several `children` nodes. The structure will be further clarified in the following example which explains a way of visualizing the parse tree.

Example:
```python
import json
from pyleri import Choice
from pyleri import Grammar
from pyleri import Keyword
from pyleri import Regex
from pyleri import Repeat
from pyleri import Sequence


# Create a Grammar Class to define your language
class MyGrammar(Grammar):
    r_name = Regex('(?:"(?:[^"]*)")+')
    k_hi = Keyword('hi')
    k_bye = Keyword('bye')
    START = Repeat(Sequence(Choice(k_hi, k_bye), r_name))


# Returns properties of a node object as a dictionary:
def node_props(node, children):
    return {
        'start': node.start,
        'end': node.end,
        'name': node.element.name if hasattr(node.element, 'name') else None,
        'element': node.element.__class__.__name__,
        'string': node.string,
        'children': children}


# Recursive method to get the children of a node object:
def get_children(children):
    return [node_props(c, get_children(c.children)) for c in children]


# View the parse tree:
def view_parse_tree(res):
    start = res.tree.children[0] \
        if res.tree.children else res.tree
    return node_props(start, get_children(start.children))


if __name__ == '__main__':
    # Compile your grammar by creating an instance of the Grammar Class:
    my_grammar = MyGrammar()
    res = my_grammar.parse('hi "siri" bye "siri"')
    # The parse tree is visualized as a JSON object:
    print(json.dumps(view_parse_tree(res), indent=2))
```

Part of the output is shown below.

```json

    {
    "start": 0,
    "end": 23,
    "name": "START",
    "element": "Repeat",
    "string": "hi \"pyleri\" hi \"pyleri\"",
    "children": [
        {
        "start": 0,
        "end": 11,
        "name": null,
        "element": "Sequence",
        "string": "hi \"pyleri\"",
        "children": [
            {
            "start": 0,
            "end": 2,
            "name": null,
            "element": "Choice",
            "string": "hi",
            "children": [
                {
                "start": 0,
                "end": 2,
                "name": "k_hi",
                "element": "Keyword",
                "string": "hi",
                "children": []
                }
            ]
            },
            {
            "start": 3,
            "end": 11,
            "name": "r_name",
            "element": "Regex",
            "string": "\"pyleri\"",
            "children": []
            }

            "..."
            "..."


```
A node contains 5 properties that will be explained next:

- `start` property returns the start of the node object.
- `end` property returns the end of the  node object.
- `element` returns the type of [Element](#elements) (e.g. Repeat, Sequence, Keyword, etc.). An element can be assigned to a variable; for instance in the example above `Keyword('hi')` was assigned to `k_hi`. With `element.name` the assigned name `k_hi` will be returned. Note that it is not a given that an element is named; in our example `Sequence` was not assigned, thus in this case the element has no attribute `name`.
- `string` returns the string that is parsed.
- `children` can return a node object containing deeper layered nodes provided that there are any. In our example the root node has an element type `Repeat()`, starts at 0 and ends at 24, and it has two `children`. These children are node objects that have both an element type `Sequence`, start at 0 and 12 respectively, and so on.


### Expecting
`expecting` returns a Python set() containing elements which pyleri expects at `pos`. Even if `is_valid` is true there might be elements in this set, for example when an `Optional()` element could be added to the string. Expecting is useful if you want to implement things like auto-completion, syntax error handling, auto-syntax-correction etc. The following example will illustrate a way of implementation.

Example:
```python
import re
import random
from pyleri import Choice
from pyleri import Grammar
from pyleri import Keyword
from pyleri import Repeat
from pyleri import Sequence
from pyleri import end_of_statement


# Create a Grammar Class to define your language.
class MyGrammar(Grammar):
    RE_KEYWORDS = re.compile(r'\S+')
    r_name = Keyword('"pyleri"')
    k_hi = Keyword('hi')
    k_bye = Keyword('bye')
    START = Repeat(Sequence(Choice(k_hi, k_bye), r_name), mi=2)


# Print the expected elements as a indented and numbered list.
def print_expecting(node_expecting, string_expecting):
    for loop, e in enumerate(node_expecting):
        string_expecting = '{}\n\t({}) {}'.format(string_expecting, loop, e)
    print(string_expecting)


# Complete a string until it is valid according to the grammar.
def auto_correction(string, my_grammar):
    node = my_grammar.parse(string)
    print('\nParsed string: {}'.format(node.tree.string))

    if node.is_valid:
        string_expecting = 'String is valid. \nExpected: '
        print_expecting(node.expecting, string_expecting)

    else:
        string_expecting = 'String is NOT valid.\nExpected: ' \
            if not node.pos \
            else 'String is NOT valid. \nAfter "{}" expected: '.format(
                                                  node.tree.string[:node.pos])
        print_expecting(node.expecting, string_expecting)

        selected = random.choice(list(node.expecting))
        string = '{} {}'.format(node.tree.string[:node.pos],
                                selected
                                if selected
                                is not end_of_statement else '')

        auto_correction(string, my_grammar)


if __name__ == '__main__':
    # Compile your grammar by creating an instance of the Grammar Class.
    my_grammar = MyGrammar()
    string = 'hello "pyleri"'
    auto_correction(string, my_grammar)

```

Output:
```
Parsed string: hello "pyleri"
String is NOT valid.
Expected:
        (1) hi
        (2) bye

Parsed string:  bye
String is NOT valid.
After " bye" expected:
        (1) "pyleri"

Parsed string:  bye "pyleri"
String is NOT valid.
After " bye "pyleri"" expected:
        (1) hi
        (2) bye

Parsed string:  bye "pyleri" hi
String is NOT valid.
After " bye "pyleri" hi" expected:
        (1) "pyleri"

Parsed string:  bye "pyleri" hi "pyleri"
String is valid.
Expected:
        (1) hi
        (2) bye

```
In the above example we parsed an invalid string according to the grammar class. The `auto-correction()` method that we built for this example combines all properties from the `parse()` to create a valid string. The output shows every recursion of the `auto-correction()` method and prints successively the set of expected elements. It takes one randomly and adds it to the string. When the string corresponds to the grammar, the property `is_valid` will return `True`. Notably the `expecting` property still contains elements even if the `is_valid` returned `True`. The reason in this example is because of the [Repeat](#repeat) element.

## Elements
Pyleri has several elements which are all subclasses of [Element](#element) and can be used to create a grammar.

### Keyword
syntax:
```python
Keyword(keyword, ign_case=False)
```
The parser needs to match the keyword which is just a string. When matching keywords we need to tell the parser what characters are allowed in keywords. By default Pyleri uses `^\w+` which is both in Python and JavaScript equal to `^[A-Za-z0-9_]+`. We can overwrite the default by setting `RE_KEYWORDS` in the grammar. Keyword() accepts one keyword argument `ign_case` to tell the parser if we should match case insensitive.

Example:

```python
class TicTacToe(Grammar):
    # Let's allow keywords with alphabetic characters and dashes.
    RE_KEYWORDS = re.compile('^[A-Za-z-]+')

    START = Keyword('tic-tac-toe', ign_case=True)

ttt_grammar = TicTacToe()
ttt_grammar.parse('Tic-Tac-Toe').is_valid  # => True
```

### Regex
syntax:
```python
Regex(pattern, flags=0)
```
The parser compiles a regular expression using the `re` module. The current version of pyleri has only support for the `re.IGNORECASE` flag.
See the [Quick usage](#quick-usage) example for how to use `Regex`.

### Token
syntax:
```python
Token(token)
```
A token can be one or more characters and is usually used to match operators like `+`, `-`, `//` and so on. When we parse a string object where pyleri expects an element, it will automatically be converted to a `Token()` object.

Example:
```python
class Ni(Grammar):
    t_dash = Token('-')
    # We could just write delimiter='-' because
    # any string will be converted to Token()
    START = List(Keyword('ni'), delimiter=t_dash)

ni = Ni()
ni.parse('ni-ni-ni-ni-ni').is_valid  # => True
```

### Tokens
syntax:
```python
Tokens(tokens)
```
Can be used to register multiple tokens at once. The `tokens` argument should be a string with tokens separated by spaces. If given tokens are different in size the parser will try to match the longest tokens first.

Example:
```python
class Ni(Grammar):
    tks = Tokens('+ - !=')
    START = List(Keyword('ni'), delimiter=tks)

ni = Ni()
ni.parse('ni + ni != ni - ni').is_valid  # => True
```

### Sequence
syntax:
```python
Sequence(element, element, ...)
```
The parser needs to match each element in a sequence.

Example:
```python
class TicTacToe(Grammar):
    START = Sequence(Keyword('Tic'), Keyword('Tac'), Keyword('Toe'))

ttt_grammar = TicTacToe()
ttt_grammar.parse('Tic Tac Toe').is_valid  # => True
```

### Choice
syntax:
```python
Choice(element, element, ..., most_greedy=True)
```
The parser needs to choose between one of the given elements. Choice accepts one keyword argument `most_greedy` which is `True` by default. When `most_greedy` is set to `False` the parser will stop at the first match. When `True` the parser will try each element and returns the longest match. Setting `most_greedy` to `False` can provide some extra performance. Note that the parser will try to match each element in the exact same order they are parsed to Choice.

Example: let us use `Choice` to modify the Quick usage example to allow the string 'bye "Iris"'
```python
class MyGrammar(Grammar):
    r_name = Regex('(?:"(?:[^"]*)")+')
    k_hi = Keyword('hi')
    k_bye = Keyword('bye')
    START = Sequence(Choice(k_hi, k_bye), r_name)

my_grammar = MyGrammar()
my_grammar.parse('hi "Iris"').is_valid  # => True
my_grammar.parse('bye "Iris"').is_valid  # => True
```

### Repeat
syntax:
```python
Repeat(element, mi=0, ma=None)
```
The parser needs at least `mi` elements and at most `ma` elements. When `ma` is set to `None` we allow unlimited number of elements. `mi` can be any integer value equal or higher than 0 but not larger then `ma`.

Example:
```python
class Ni(Grammar):
    START = Repeat(Keyword('ni'))

ni = Ni()
ni.parse('ni ni ni ni ni').is_valid  # => True
```

It is not allowed to bind a name to the same element twice and Repeat(element, 1, 1) is a common solution to bind the element a second (or more) time(s).

For example consider the following:
```python
class MyGrammar(Grammar):
    r_name = Regex('(?:"(?:[^"]*)")+')

    # Raises a SyntaxError because we try to bind a second time.
    r_address = r_name # WRONG

    # Instead use Repeat
    r_address = Repeat(r_name, 1, 1) # RIGHT
```

### List
syntax:
```python
List(element, delimiter=',', mi=0, ma=None, opt=False)
```
List is like Repeat but with a delimiter. A comma is used as default delimiter but any element is allowed. When a string is used as delimiter it will be converted to a `Token` element. `mi` and `ma` work exactly like with Repeat. An optional keyword argument `opt` can be set to `True` to allow the list to end with a delimiter. By default this is set to `False` which means the list has to end with an element.

Example:
```python
class Ni(Grammar):
    START = List(Keyword('ni'))

ni = Ni()
ni.parse('ni, ni, ni, ni, ni').is_valid  # => True
```

### Optional
syntax:
```python
Optional(element)
```
The parser looks for an optional element. It is like using `Repeat(element, 0, 1)` but we encourage to use `Optional` since it is more readable. (and slightly faster)

Example:
```python
class MyGrammar(Grammar):
    r_name = Regex('(?:"(?:[^"]*)")+')
    k_hi = Keyword('hi')
    START = Sequence(k_hi, Optional(r_name))

my_grammar = MyGrammar()
my_grammar.parse('hi "Iris"').is_valid  # => True
my_grammar.parse('hi').is_valid  # => True
```

### Ref
syntax:
```python
Ref()
```
The grammar can make a forward reference to make recursion possible. In the example below we create a forward reference to START but note that
a reference to any element can be made.

>Warning: A reference is not protected against testing the same position in
>a string. This could potentially lead to an infinite loop.
>For example:
>```python
>r = Ref()
>r = Optional(r)  # DON'T DO THIS
>```
>Use [Prio](#prio) if such recursive construction is required.

Example:
```python
class NestedNi(Grammar):
    START = Ref()
    ni_item = Choice(Keyword('ni'), START)
    START = Sequence('[', List(ni_item), ']')

nested_ni = NestedNi()
nested_ni.parse('[ni, ni, [ni, [], [ni, ni]]]').is_valid  # => True
```

### Prio
syntax:
```python
Prio(element, element, ...)
```
Choose the first match from the prio elements and allow `THIS` for recursive operations. With `THIS` we point to the `Prio` element. Probably the example below explains how `Prio` and `THIS` can be used.

>Note: Use a [Ref](#ref) when possible.
>A `Prio` element is required when the same position in a string is potentially
>checked more than once.

Example:
```python
class Ni(Grammar):
    k_ni = Keyword('ni')
    START = Prio(
        k_ni,
        # '(' and ')' are automatically converted to Token('(') and Token(')')
        Sequence('(', THIS, ')'),
        Sequence(THIS, Keyword('or'), THIS),
        Sequence(THIS, Keyword('and'), THIS))

ni = Ni()
ni.parse('(ni or ni) and (ni or ni)').is_valid  # => True
```
