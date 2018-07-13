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