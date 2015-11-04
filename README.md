Python Left-Right Parser
========================

Why Pyleri?
-----------
Pyleri is an easy-to-use parser create for SiriDB. We first used [lrparsing](http://lrparsing.sourceforge.net/doc/html/) and wrote [jsleri](https://github.com/transceptor-technology/jsleri) for auto-completion and suggestions in our web console. Later we found small issues in lrparsing and also had difficulties keeping the language the same in both projects. That's when we decided to create Pyleri which can export a created language to JavaScript.


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
my_grammer = MyGrammar()

# Use the compiled grammar to parse 'strings'
print(my_grammer.parse('hi "Iris"').is_valid) # => True
print(my_grammer.parse('bye "Iris"').is_valid) # => False
```

parse() method
--------------
The `parse()` method returns a `NodeResult` object which has the following properties:
- `expecting`: A Python set() containing pyleri objects which pyleri expects at `pos`
- `is_valid`: Boolean value, `True` when the given string is valid, `False` when not valid.
- `pos`: Position where the parser had to stop. (when `is_valid` is `True` this value will be equal to the length of the given string)
- `tree`: Contains the parse tree

Let's take the example from Quick usage.
```python
node_result = my_grammer.parse('bye "Iris"')
print(node_result.is_valid) # => False
print(node_result.expecting) # => {hi} => We expected Keyword 'hi' instead of bye 
print(node_result.pos) # => 0 => Position in the string where we are expecting the above
print(node_result.tree) # => Node object containing the parse tree
```

Choice
------
syntax:
```python
Choice(PyleriObject, PyleriObject, ..., [most_greedy=True/False])
```
The parser needs to choose between one of the given PyleriObjects. Choice accepts one keyword argument `most_greedy` which is `True` by default. When `most_greedy` is set to `False` the parser will stop at the first match and `choose` that object. When `True` the parser will try each PyleriObject and returns the longest match. Settings `most_greedy` to `False` can provide some extra performance. Note that the parser will try to match each PyleriObject in the exact same order they are parsed to Choice.

Example: let's use `Choice` to modify the Quick usage example to allow the string 'bye "Iris"'
```python
class MyGrammar(Grammar):
    r_name = Regex('(?:"(?:[^"]*)")+')
    k_hi = Keyword('hi')
    k_bye = Keyword('bye')
    START = Sequence(Choice(k_hi, k_bye), r_name)
```
