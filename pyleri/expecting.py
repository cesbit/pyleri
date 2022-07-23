"""Expecting Class.

Expecting Class is used to return possible elements at a position when a given
statement is not correct. This helps building auto-completion, suggestions or
returning nice messages to the user.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
"""
import typing as t
if t.TYPE_CHECKING:
    from .elements import Element


class Expecting:

    __slots__ = ('required', 'optional', 'pos', '_modes')

    def __init__(self):
        self.required: t.Set['Element'] = set()
        self.optional: t.Set['Element'] = set()
        self.pos: int = 0
        self._modes: t.Dict[int, t.Set['Element']] = {self.pos: self.required}

    def set_mode_required(self, pos: int, is_required: bool):
        # do nothing when mode is already set to optional
        if pos in self._modes and self._modes[pos] is self.optional:
            return

        self._modes[pos] = self.required if is_required else self.optional

    def empty(self):
        self.required.clear()
        self.optional.clear()

    def update(self, element: 'Element', pos: int):
        if pos > self.pos:
            self.empty()
            self.pos = pos

        if pos == self.pos:
            self._modes[pos].add(element)

    def get_expecting(self) -> t.Set['Element']:
        return self.required | self.optional
