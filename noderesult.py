class NodeResult:

    __slots__ = ('is_valid', 'pos', 'expecting', 'tree')

    def __init__(self, is_valid, pos):
        self.is_valid = is_valid
        self.pos = pos
        self.expecting = None
        self.tree = None
