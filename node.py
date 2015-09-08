class Node:

    __slots__ = ('element', 'start', 'end', 'string', 'children')

    def __init__(self, element, start, end=None, string=None):
        self.element = element
        self.start = start
        self.end = end
        self.string = string
        self.children = []
