Python Left-Right Parser
========================

Why Pyleri?
-----------
Pyleri is an easy-to-use parser create for SiriDB. We first used [lrparsing](http://lrparsing.sourceforge.net/doc/html/) and wrote [jsleri](https://github.com/transceptor-technology/jsleri) for auto-completion and suggestions in our web console. Later we found small issues in lrparsing and also had difficulties keeping the language the same in both projects. That's when we decided to create Pyleri which can export a created language to JavaScript.


Quick usage
-----------
```python
# Imports
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
myGrammer = MyGrammar()

# Use the compiled grammar to parse 'strings'
print(myGrammer.parse('hi "Iris"').is_valid)  # => True
print(myGrammer.parse('bye "Iris"').is_valid)  # => False
```

parse() method
--------------
The `parse()` method returns a `NodeResult` object which has the following properties:
- `expecting`: A Python set() containing pyleri objects which pyleri expects at `pos`
- `is_valid`: Boolean value, `True` when the given string is valid, `False` when not valid.
- `pos`: Position where the parser had to stop. (this is equals to the length of the given string when `is_valid` is `True`)
- `tree`: Contains the parse tree
