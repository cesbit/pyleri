'''Element and NamedElement Class.

These are the base classes used for all other elements.

:copyright: 2021, Jeroen van der Heijden <jeroen@cesbit.com>
'''


def camel_case(s):
    return ''.join(
        p[0].upper() + p[1:] if n else p
        for n, p in enumerate(s.split('_')))


def cap_case(s):
    return ''.join(p[0].upper() + p[1:] for p in s.split('_') if p)


_cref = None


def c_export(func):

    def wrapper(self, c_indent, indent, enums, ref=None):
        global _cref
        elem, _cref = self if _cref is None else _cref, ref
        gid = getattr(elem, 'name', getattr(elem, '_name', 'CLERI_NONE'))
        if gid != 'CLERI_NONE':
            gid = 'CLERI_GID_{}'.format(gid.upper())
            enums.add(gid)

        return func(self, c_indent, indent, enums, gid)

    return wrapper


def go_export(func):

    def wrapper(self, go_indent, indent, enums):
        gid = getattr(self, 'name', getattr(self, '_name', 'NoGid'))
        if gid != 'NoGid':
            gid = 'Gid{}'.format(cap_case(gid))
            enums.add(gid)
        return func(self, go_indent, indent, enums, gid)

    return wrapper


def java_export(func):

    def wrapper(self, java_indent, indent, enums, classes):
        classes.add('jleri.{}'.format(self.__class__.__name__.lstrip('_')))
        gid = getattr(self, 'name', getattr(self, '_name', None))
        if gid is not None:
            gid = gid.upper()
            enums.add(gid)
        return func(self, java_indent, indent, enums, classes, gid)

    return wrapper


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

    def _export_js(self, js_indent, indent, classes, cname):
        classes.add(self.__class__.__name__.lstrip('_'))
        if hasattr(self, 'name') and indent > 0:
            return '{}.{}'.format(cname, self.name) if cname else self.name
        indent = 0 if indent < 0 else 1 if indent == 0 else indent
        return self._run_export_js(js_indent, indent, classes, cname)

    def _export_js_elements(self, js_indent, indent, classes, cname):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=js_indent * new_indent,
            elem=elem._export_js(
                js_indent,
                new_indent, classes, cname)) for elem in self._elements])
        return '{class_name}(\n{value}\n{indent})'.format(
            class_name=self.__class__.__name__.lstrip('_'),
            value=value,
            indent=js_indent * indent)

    def _run_export_js(self, js_indent, indent, classes, cname):
        return 'not_implemented'

    def _export_py(self, py_indent, indent, classes):
        classes.add(self.__class__.__name__.lstrip('_'))
        if hasattr(self, 'name') and indent:
            return self.name
        return self._run_export_py(py_indent, indent or 1, classes)

    def _export_py_elements(self, py_indent, indent, classes):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=py_indent * new_indent,
            elem=elem._export_py(
                py_indent,
                new_indent, classes)) for elem in self._elements])
        return '{class_name}(\n{value}\n{indent})'.format(
            class_name=self.__class__.__name__.lstrip('_'),
            value=value,
            indent=py_indent * indent)

    def _run_export_py(self, py_indent, indent, classes):
        return 'not_implemented'

    @c_export
    def _export_c(self, c_indent, indent, enums, gid):
        if hasattr(self, 'name') and indent:
            return self.name
        return self._run_export_c(c_indent, indent or 1, enums)

    @c_export
    def _export_c_elements(self, c_indent, indent, enums, gid):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=c_indent * new_indent,
            elem=elem._export_c(
                c_indent,
                new_indent,
                enums)) for elem in self._elements])
        return \
            'cleri_{class_name}(\n{gid},\n{num},\n{value}\n{indent})'.format(
                class_name=self.__class__.__name__.lstrip('_').lower(),
                gid='{indent}{gid}'.format(
                    indent=c_indent * (indent + 1),
                    gid=gid),
                num='{indent}{num}'.format(
                    indent=c_indent * (indent + 1),
                    num=len(self._elements)),
                value=value,
                indent=c_indent * indent)

    def _run_export_c(self, c_indent, indent, enums):
        return 'not_implemented'

    @go_export
    def _export_go(self, go_indent, indent, enums, gid):
        if hasattr(self, 'name') and indent:
            return camel_case(self.name)
        return self._run_export_go(go_indent, indent or 1, enums)

    @go_export
    def _export_go_elements(self, go_indent, indent, enums, gid):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=go_indent * new_indent,
            elem=elem._export_go(
                go_indent,
                new_indent,
                enums)) for elem in self._elements])
        return '{class_name}(\n{gid},\n{value},\n{indent})'.format(
            class_name='goleri.New' + self.__class__.__name__.lstrip('_'),
            gid='{indent}{gid}'.format(
                indent=go_indent * (indent + 1),
                gid=gid),
            value=value,
            indent=go_indent * indent)

    def _run_export_go(self, go_indent, indent, enums):
        return 'not_implemented'

    @java_export
    def _export_java(self, java_indent, indent, enums, classes, gid):
        if hasattr(self, 'name') and indent > 0:
            return self.name.upper()
        return self._run_export_java(
            java_indent, abs(indent) or 1, enums, classes)

    @java_export
    def _export_java_elements(
            self, java_indent, indent, enums, classes, gid):
        new_indent = indent + 1
        value = ',\n'.join(['{indent}{elem}'.format(
            indent=java_indent * new_indent,
            elem=elem._export_java(
                java_indent,
                new_indent,
                enums,
                classes)) for elem in self._elements])
        return '{class_name}({gid}\n{value}\n{indent})'.format(
            class_name='new ' + self.__class__.__name__.lstrip('_'),
            gid='' if gid is None else '\n{indent}Ids.{gid},'.format(
                indent=java_indent * (indent + 1),
                gid=gid),
            value=value,
            indent=java_indent * indent)

    def _run_export_java(self, java_indent, indent, enums, classes):
        return 'not_implemented'

# Added this import to the bottom to prevent circular import cycle.
# Note: usually this is bad design but in this case we do want class
#       inheritance which allows us to create a new class Token which
#       is sub-classed from the 'NamedElement' class.


from .token import Token  # nopep8
