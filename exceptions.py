class CompileError(Exception):
    pass


class KeywordError(CompileError):
    pass


class ReKeywordsChangedError(CompileError):
    pass


class NameAssignedError(CompileError):
    pass
