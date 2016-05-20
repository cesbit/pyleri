'''Exceptions.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
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