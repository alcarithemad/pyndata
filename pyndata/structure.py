from __future__ import absolute_import

import copy

try: from cStringIO import StringIO
except: from StringIO import StringIO

from .field import __nextfield__
from .field import Field
from .bitfield import BitField
from .structfield import StructField

# This is a little strange, so it deserves an explanation.
# In StructMeta down below, we need to check if the newly created class is
# a Struct, but the real Struct class doesn't exist yet, and won't exist
# when it's being run through the __new__ method.
#
# Instead, we "forward declare" Struct here a la C, then inherit from this
# Struct in the real Struct class below. If it helps, mentally replace every
# "Struct" before "class Struct(object" (and the on in the base classes there)
# with "FirstStruct".
class Struct:
    pass

class StructMeta(type):
    def __new__(cls, cls_name, bases, attrs):
        fields = []
        bitfields = []
        field_defaults = {}
        for name, field in attrs.items():
            if issubclass(type(field), Field):
                field.name = name
                if name[0] == '_':
                    field.__SHOW__ = False
                field_defaults[name] = field.default
                fields.append(field)
            elif issubclass(type(field), BitField):
                field.name = name
                bitfields.append(field)
            elif issubclass(type(field), Struct):
                sf = StructField(field)
                sf.name = name
                if name[0] == '_':
                    sf.__SHOW__ = False
                field_defaults[name] = sf.default
                fields.append(sf)
                attrs[name] = sf
        fields.sort(key=lambda x:x.index)
        new_cls = type.__new__(cls, cls_name, bases, attrs)
        new_cls.field_defaults = field_defaults
        new_cls.__FIELDS__ = fields
        new_cls.bitfields = bitfields
        return new_cls

class Struct(object, Struct):
    __metaclass__ = StructMeta
    __ENDIAN__ = 'little'

    def __init__(self, initial=None):
        self.index = __nextfield__()
        self.field_items = copy.deepcopy(self.field_defaults)
        for field in self.__FIELDS__:
            for linked in field.linked_fields:
                linked.owner = self
        if initial:
            self.unpack(initial)

    def __repr__(self):
        fields = [field.name+'='+repr(getattr(self, field.name)) for field in self.__FIELDS__ if field.__SHOW__]
        fields.extend(field.name+'='+repr(field.__get__(self)) for field in self.bitfields if field.__SHOW__)
        ret = '{0}({1})'.format(type(self).__name__, ', '.join(fields))
        return ret

    def pack(self):
        out = []
        for field in self.__FIELDS__:
            out.append(field.pack(self.field_items[field.name], self))
        return ''.join(out)

    def unpack(self, reader):
        if isinstance(reader, str):
            reader = StringIO(reader)
        for field in self.__FIELDS__:
            self.field_items[field.name] = field.unpack(reader, self)
