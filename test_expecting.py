import json
import re
from pyleri import Choice
from pyleri import Grammar
from pyleri import Keyword
from pyleri import Regex
from pyleri import Repeat
from pyleri import Sequence
from pyleri import Token


# Create a Grammar Class to define your language
class MyGrammar(Grammar):
    # RE_KEYWORDS = re.compile('\S+')
    k_all = Token('*')
    k_mean = Token('mean')
    k_serie = Token('series-001')
    k_select = Token('select')
    k_from = Token('from')
    START = Sequence(k_select,
                     Choice(k_mean, k_all),
                     k_from,
                     Choice(k_serie, k_all))


def is_not_int(v):
    try:
        i = int(v)
    except:
        return True
    return False


def auto_completion(rawinput, my_grammar):
    print(rawinput)
    node = my_grammar.parse(rawinput)
    # print(node.pos)
    if node.is_valid:
        print('String is valid')

    else:
        expect = [e for e in node.expecting]
        string_expecting = '\nExpecting: '
        loop = 0

        for e in expect:
            loop += 1
            string_expecting = string_expecting + '\n({}) {}'.format(loop, e)
        print(string_expecting)

        choice = input('Choose a integer between 1-{}: '.format(len(expect)))

        while is_not_int(choice):
            choice = \
                input('Choose a integer between 1-{}: '.format(len(expect)))

        while int(choice) not in range(1, len(expect)+1):
            choice = \
                input('Choose a integer between 1-{}: '.format(len(expect)))

        auto_completion(rawinput[0:node.pos] + ' ' + str(expect[int(choice) - 1]), my_grammar)




if __name__ == '__main__':
    # Compile your grammar by creating an instance of the Grammar Class.
    my_grammar = MyGrammar()
    rawinput = input('Write a query starting with "select": ')
    auto_completion(rawinput, my_grammar)


# if loop == 1:
            #     string = string + '\n({}) {}'.format(loop, e)
            # elif loop == (len(expect)):
            #     string = string + ' or\n({}) {}'.format(loop, e)
            # else:
            #     string = string + ',\n({}) {}'.format(loop, e)

            #r = str(expect[int(choice) - 1]) if expect[int(choice) - 1] is not MyGrammar.r_name else '"pyleri"'