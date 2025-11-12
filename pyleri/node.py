"""Node class.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
"""
import typing as t
if t.TYPE_CHECKING:
    from .elements import Element


class Node:

    __slots__ = ('element', '_string', 'start', 'end', 'children')

    def __init__(
            self,
            element: 'Element',
            string: str,
            start: int,
            end: t.Optional[int] = None):
        self.element = element
        self.start = start
        self.end = end or 0
        self._string = string
        self.children: t.List['Node'] = []

    @property
    def string(self) -> str:
        return self._string[self.start:self.end]
