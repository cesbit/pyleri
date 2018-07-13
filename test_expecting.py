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
    RE_KEYWORDS = re.compile('\S+')
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
