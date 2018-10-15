'''Result class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''
from .keyword import Keyword
from .token import Token
from .tokens import Tokens
from .endofstatement import _EndOfStatement


TOSTR = (Keyword, Token, Tokens, _EndOfStatement)


class Result:

    __slots__ = ('is_valid', 'pos', 'expecting', 'tree')

    def __init__(self, is_valid, pos):
        self.is_valid = is_valid
        self.pos = pos
        self.expecting = None
        self.tree = None

    def as_str(self, translate=None):
        if self.is_valid:
            return 'parsed successfully'
        res = [f'error at position {self.pos}']
        arr = []
        for elem in (self.expecting):
            expectstr = translate(elem) if translate else None
            if expectstr is None and isinstance(elem, TOSTR):
                expectstr = str(elem)

            if expectstr:
                arr.append(expectstr)

        arr.sort()
        total = len(arr) - 1
        for i, expectstr in enumerate(arr):
            if i == 0:
                res.append(f', expecting: {expectstr}')
            elif i < total:
                res.append(f', {expectstr}')
            else:
                res.append(f' or {expectstr}')

        return ''.join(res)

    def __str__(self):
        return self.as_str()
