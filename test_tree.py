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


def node_params(node, children):
    return {
        'start': node.start,
        'end': node.end,
        'name': node.element.name if hasattr(node.element, 'name') else None,
        'element': node.element.__class__.__name__,
        'string': node.string,
        'children': children}


def get_children(children):
    return [node_params(c, get_children(c.children)) for c in children]


def view_parse_tree(node_result):
    start = node_result.tree.children[0] \
        if node_result.tree.children else node_result.tree
    return node_params(start, get_children(start.children))


if __name__ == '__main__':
    # Compile your grammar by creating an instance of the Grammar Class.
    my_grammar = MyGrammar()
    node_result = my_grammar.parse('hi "pyleri" bye "pyleri"')
    print(node_result.is_valid)
    print(node_result.pos)
    print(json.dumps(view_parse_tree(node_result), indent=2))
