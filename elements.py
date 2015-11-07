'''Element and NamedElement Class.

These are the base classes used for all other elements.

:copyright: 2015, Jeroen van der Heijden (Transceptor Technology)
:license: need to decide
'''


class Element:

    __slots__ = tuple()

    @staticmethod
    def _validate_element(element):
        if isinstance(element, str):
            return Token(element)
        if isinstance(element, Element):
            return element
        raise TypeError(
            'Expecting an element or string but received type: {}'.format(
                type(element)))

    @classmethod
    def _validate_elements(cls, elements):
        return [cls._validate_element(elem) for elem in elements]


class NamedElement(Element):

    __slots__ = ('name',)

    def _export_js(self, js_identation, ident, classes):
        classes.add(self.__class__.__name__.lstrip('_'))
        if hasattr(self, 'name') and ident:
            return self.name
        elif hasattr(self, '_elements'):
            return self._export_js_elements(js_identation, ident or 1, classes)
        else:
            return self._new_export_js(js_identation, ident or 1, classes)

    def _export_js_elements(self, js_identation, ident, classes):
        new_ident = ident + 1
        value = ',\n'.join(['{ident}{elem}'.format(
            ident=js_identation * new_ident,
            elem=elem._export_js(
                js_identation,
                new_ident, classes)) for elem in self._elements])
        return '{class_name}(\n{value}\n{ident})'.format(
            class_name=self.__class__.__name__.lstrip('_'),
            value=value,
            ident=js_identation * ident)

    def _new_export_js(self, js_identation, ident, classes):
        return 'not_implemented'

# Added this import to the bottom to prevent circular import cycle.
# Note: usually this is bad design but in this case we do want class
#       inheritance which allows us to create a new class Token which
#       is sub-classed from the 'NamedElement' class.
from .token import Token  # nopep8
