'''Exceptions.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''


class CompileError(Exception):
    pass


class KeywordError(CompileError):
    pass


class ReKeywordsChangedError(CompileError):
    pass


class NameAssignedError(CompileError):
    pass


class MissingRefError(CompileError):
    pass


class MissingStartError(CompileError):
    pass


class UnusedElementError(CompileError):
    pass


class ParseError(Exception):
    pass


class MaxRecursionError(ParseError):
    pass
