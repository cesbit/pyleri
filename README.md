Python Left-Right Parser
========================

Why Pyleri?
-----------
Pyleri is an easy-to-use parser created for SiriDB. We first used [lrparsing](http://lrparsing.sourceforge.net/doc/html/) and wrote [jsleri](https://github.com/transceptor-technology/jsleri) for auto-completion and suggestions in our web console. Later we found small issues in lrparsing and also had difficulties keeping the language the same in both projects. That is when we decided to create Pyleri which can export a created language to JavaScript.

Installation
------------
The easiest way is to use PyPI:

    sudo pip3 install trender

Quick usage
-----------
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
```

Grammar
-------
When writing a grammar you should subclass Grammar. A Grammar expects at least a `START` property so the parser knows where to start parsing. Grammar has some default properties which can be overwritten like `RE_KEYWORDS` and `RE_WHITESPACE`, which are both explained later. Grammer also has two methods: `parse()` and `export_js()` which are explained below.

Grammar.parse()
---------------
syntax:
```python
Grammar.parse(string)
```
The `parse()` method returns a `NodeResult` object which has the following properties:
- `expecting`: A Python set() containing elements which pyleri expects at `pos`. Even if `is_valid` is true there might be elements in this set, for example when an `Optional()` element could be added to the string.
- `is_valid`: Boolean value, `True` when the given string is valid, `False` when not valid.
- `pos`: Position where the parser had to stop. (when `is_valid` is `True` this value will be equal to the length of the given string with `str.rstrip()` applied)
- `tree`: Contains the parse tree. Even when `is_valid` is `False` the parse tree is returned but will only contain results as far as parsing has succeeded.

Let us take the example from Quick usage.
```python
node_result = my_grammer.parse('bye "Iris"')
print(node_result.is_valid) # => False
print(node_result.expecting) # => {hi} => We expected Keyword 'hi' instead of bye 
print(node_result.pos) # => 0 => Position in the string where we are expecting the above
print(node_result.tree) # => Node object containing the parse tree
```

Grammar.export_js()
-------------------
syntax:
```python
Grammar.export_js(
    js_module_name='jsleri', 
    js_template=Grammar.JS_TEMPLATE, 
    js_identation=' ' * 4)
```
Optional keyword arguments:
- `js_module_name`: Name of the JavaScript module. (default: 'jsleri')
- `js_template`: Template String used for the export. You might want to look at the default string which can be found at Grammar.JS_TEMPLATE.
- `js_identation`: identation used in the JavaScript file. (default: 4 spaces)

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

Choice
------
syntax:
```python
Choice(element, element, ..., most_greedy=True)
```
The parser needs to choose between one of the given elements. Choice accepts one keyword argument `most_greedy` which is `True` by default. When `most_greedy` is set to `False` the parser will stop at the first match. When `True` the parser will try each element and returns the longest match. Settings `most_greedy` to `False` can provide some extra performance. Note that the parser will try to match each element in the exact same order they are parsed to Choice.

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

Sequence
--------
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

Keyword
-------
syntax:
```python
Keyword(keyword, ign_case=Fasle)
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

Repeat
------
syntax:
```python
Repeat(element, mi=0, ma=None)
```
The parser needs at least `mi` elements and at most `ma` elements. When `ma` is set to `None` we allow unlimited number of elements. `mi` can be any integer value equal of higher than 0 but not larger then `ma`.

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

List
----
syntax:
```python
List(element, delimiter=',', mi=0, ma=None, opt=False)
```
List is like Repeat but with a delimiter. A comma is used as default delimiter but any element is allowed. When a string is used as delimiter it will be converted to a `Token` element. `mi` and `ma` work excatly like with Repeat. An optional keyword argument `opt` can be set to `True` to allow the list to end with a delimiter. By default this is set to `False` which means the list has to end with an element.

Example:
```python
class Ni(Grammar):
    START = List(Keyword('ni'))

ni = Ni()
ni.parse('ni, ni, ni, ni, ni').is_valid  # => True
```

Optional
--------
syntax:
```python
Optional(element)
```
The pasrser looks for an optional element. It is like using `Repeat(element, 0, 1)` but we encourage to use `Optional` since it is more readable. (and slightly faster)

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

Regex
-----
syntax:
```python
Regex(pattern, flags=0)
```
The parser compiles a regular expression using the `re` module. Therefore information about `flags` can be found at https://docs.python.org/3/library/re.html

See the Quick Usage example for how to use `Regex`.

Token
-----
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

Tokens
------
syntax:
```python
Tokens(tokens)
```
Can be used to register multiple tokens at once. The `tokens` argument should be a string with tokens seperated by spaces. If given tokens are different in size the parser will try to match the longest tokens first.

Example:
```python
class Ni(Grammar):
    tks = Tokens('+ - !=')
    START = List(Keyword('ni'), delimiter=tks)

ni = Ni()
ni.parse('ni + ni != ni - ni').is_valid  # => True
```

Prio
----
syntax:
```python
Prio(element, element, ...)
```
Choose the first match from the prio elements and allow `THIS` for recursive operations. With `THIS` we point to the `Prio` element. Probably the example below explains how `Prio` and `THIS` can be used.

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
        
