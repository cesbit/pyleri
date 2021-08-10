'''pyleri.Ref Class.

When a forward reference is used the grammar must contain a final
reference with the same name. The Grammar class is used to validate
a valid grammer and set element.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''
from .elements import NamedElement


class Ref(NamedElement):
    '''Ref class.'''

    __slots__ = ('_element', '_get_node_result')

    @property
    def element(self):
        return getattr(self, '_element', None)

    @element.setter
    def element(self, element):
        self._element = self._validate_element(element)
        self._get_node_result = self._element._get_node_result

    def _run_export_js(self, js_indent, indent, classes, cname):
        return 'Ref({})'.format(self._element.__class__.__name__)

    def _run_export_py(self, py_indent, indent, classes):
        return 'Ref()'

    def _run_export_c(self, c_indent, indent, enums):
        return 'cleri_ref()'

    def _run_export_go(self, go_indent, indent, classes):
        return 'goleri.NewRef()'

    def _run_export_java(self, java_indent, indent, enums, classes):
        return 'new Ref()'
