'''Node class.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
'''


class Node:

    __slots__ = ('element', '_string', 'start', 'end', 'children')

    def __init__(self, element, string, start, end=None):
        self.element = element
        self.start = start
        self.end = end
        self._string = string
        self.children = []

    @property
    def string(self):
        return self._string[self.start:self.end]
