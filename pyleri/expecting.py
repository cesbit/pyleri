'''Expecting Class.

Expecting Class is used to return possible elements at a position when a given
statement is not correct. This helps building auto-completion, suggestions or
returning nice messages to the user.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''


class Expecting:

    __slots__ = ('required', 'optional', 'pos', '_modes')

    def __init__(self):
        self.required = set()
        self.optional = set()
        self.pos = 0
        self._modes = {self.pos: self.required}

    def set_mode_required(self, pos, is_required):
        # do nothing when mode is already set to optional
        if pos in self._modes and self._modes[pos] is self.optional:
            return

        self._modes[pos] = self.required if is_required else self.optional

    def empty(self):
        self.required.clear()
        self.optional.clear()

    def update(self, element, pos):
        if pos > self.pos:
            self.empty()
            self.pos = pos

        if pos == self.pos:
            self._modes[pos].add(element)

    def get_expecting(self):
        return self.required | self.optional
