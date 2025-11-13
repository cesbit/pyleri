"""ThingsDB (v1.8.2) language file.
"""
import re
from pyleri import List
from pyleri import Repeat
from pyleri import Token
from pyleri import Grammar
from pyleri import Sequence
from pyleri import Optional
from pyleri import Tokens
from pyleri import Ref
from pyleri import Keyword
from pyleri import Prio
from pyleri import Regex
from pyleri import THIS
from pyleri import Choice

class LangDef(Grammar):
    
    RE_KEYWORDS = re.compile('^[A-Za-z_][0-9A-Za-z_]{0,254}(?![0-9A-Za-z_])')
    x_array = Token('[')
    x_assign = Tokens('+= -= *= /= %= &= ^= |= =')
    x_block = Token('{')
    x_chain = Tokens('.. .')
    x_closure = Token('|')
    x_function = Token('(')
    x_index = Token('[')
    x_parenthesis = Token('(')
    x_preopr = Regex('^(\\s*~)*(\\s*!|\\s*[\\-+](?=[^0-9]))*')
    x_ternary = Token('?')
    x_thing = Token('{')
    x_ano = Token('&{')
    x_template = Token('`')
    template = Sequence(
        x_template,
        Repeat(Choice(
            Regex('^([^`{}]|``|{{|}})+'),
            Sequence(
                Token('{'),
                THIS,
                Token('}')
            ),
            most_greedy=False), 0, None),
        x_template
    )
    t_false = Keyword('false')
    t_float = Regex(
        r'[-+]?(inf|nan|[0-9]*\.[0-9]+(e[+-][0-9]+)?)'
        r'(?![0-9A-Za-z_\.])')
    t_int = Regex(
        r'[-+]?((0b[01]+)|(0o[0-8]+)|(0x[0-9a-fA-F]+)|([0-9]+))'
        r'(?![0-9A-Za-z_\.])')
    t_nil = Keyword('nil')
    t_regex = Regex('^/((?:.(?!(?<![\\\\])/))*.?)/[a-z]*')
    t_string = Regex('^(((?:\'(?:[^\']*)\')+)|((?:"(?:[^"]*)")+))')
    t_true = Keyword('true')
    name = Regex('^[A-Za-z_][0-9A-Za-z_]{0,254}(?![0-9A-Za-z_])')
    var = Regex('^[A-Za-z_][0-9A-Za-z_]{0,254}(?![0-9A-Za-z_])')
    chain = Ref()
    closure = Sequence(
        x_closure,
        List(var, Token(','), 0, None, True),
        Token('|'),
        THIS
    )
    t_ano = Sequence(
        x_ano,
        List(Sequence(
            name,
            Token(':'),
            Optional(THIS)
        ), Token(','), 0, None, True),
        Token('}')
    )
    thing = Sequence(
        x_thing,
        List(Sequence(
            name,
            Token(':'),
            Optional(THIS)
        ), Token(','), 0, None, True),
        Token('}')
    )
    array = Sequence(
        x_array,
        List(THIS, Token(','), 0, None, True),
        Token(']')
    )
    function = Sequence(
        x_function,
        List(THIS, Token(','), 0, None, True),
        Token(')')
    )
    instance = Repeat(thing, 1, 1)
    enum_ = Sequence(
        x_thing,
        Choice(
            name,
            closure,
            most_greedy=False),
        Token('}')
    )
    opr0_mul_div_mod = Tokens('* / %')
    opr1_add_sub = Tokens('+ -')
    opr2_bitwise_shift = Tokens('<< >>')
    opr3_bitwise_and = Tokens('&')
    opr4_bitwise_xor = Tokens('^')
    opr5_bitwise_or = Tokens('|')
    opr6_compare = Tokens('== != <= >= < >')
    opr7_cmp_and = Token('&&')
    opr8_cmp_or = Token('||')
    opr9_ternary = Sequence(
        x_ternary,
        THIS,
        Token(':')
    )
    operations = Sequence(
        THIS,
        Choice(
            opr9_ternary,
            opr8_cmp_or,
            opr7_cmp_and,
            opr2_bitwise_shift,
            opr6_compare,
            opr5_bitwise_or,
            opr4_bitwise_xor,
            opr3_bitwise_and,
            opr1_add_sub,
            opr0_mul_div_mod,
            most_greedy=False),
        THIS
    )
    assign = Sequence(
        x_assign,
        THIS
    )
    name_opt_more = Sequence(
        name,
        Optional(Choice(
            function,
            assign,
            most_greedy=False))
    )
    var_opt_more = Sequence(
        var,
        Optional(Choice(
            function,
            assign,
            instance,
            enum_,
            most_greedy=False))
    )
    slice = List(Optional(THIS), Token(':'), 0, 3, False)
    index = Repeat(Sequence(
        x_index,
        slice,
        Token(']'),
        Optional(Sequence(
            x_assign,
            THIS
        ))
    ), 0, None)
    block = Sequence(
        x_block,
        List(THIS, Repeat(Token(';'), 1, None), 1, None, True),
        Token('}')
    )
    parenthesis = Sequence(
        x_parenthesis,
        THIS,
        Token(')')
    )
    k_if = Keyword('if')
    k_else = Keyword('else')
    k_return = Keyword('return')
    k_for = Keyword('for')
    k_in = Keyword('in')
    k_continue = Keyword('continue')
    k_break = Keyword('break')
    if_statement = Sequence(
        k_if,
        Token('('),
        THIS,
        Token(')'),
        THIS,
        Optional(Sequence(
            k_else,
            THIS
        ))
    )
    return_statement = Sequence(
        k_return,
        List(THIS, Token(','), 0, 3, False)
    )
    for_statement = Sequence(
        k_for,
        Token('('),
        List(var, Token(','), 1, None, False),
        k_in,
        THIS,
        Token(')'),
        THIS
    )
    expression = Sequence(
        x_preopr,
        Choice(
            chain,
            t_false,
            t_nil,
            t_true,
            t_float,
            t_int,
            t_string,
            t_regex,
            t_ano,
            template,
            var_opt_more,
            thing,
            array,
            parenthesis,
            most_greedy=False),
        index,
        Optional(chain)
    )
    statement = Prio(
        k_continue,
        k_break,
        Choice(
            if_statement,
            return_statement,
            for_statement,
            closure,
            expression,
            block,
            most_greedy=False),
        operations
    )
    START = List(statement, Repeat(Token(';'), 1, None), 0, None, True)
    chain = Sequence(
        x_chain,
        name_opt_more,
        index,
        Optional(chain)
    )
