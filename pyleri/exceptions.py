'''Exceptions.

:copyright: 2018, Jeroen van der Heijden (Transceptor Technology)
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
