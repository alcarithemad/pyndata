from __future__ import absolute_import

import copy

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from .field import __nextfield__
from .field import Field
from .structfield import StructField

# TODO: endianness

class Struct:
    pass

class StructMeta(type):
    def __new__(cls, cls_name, bases, attrs):
        fields = []
        field_defaults = {}
        for name, field in attrs.items():
            if issubclass(type(field), Field):
                field.name = name
                field_defaults[name] = field.default
                fields.append(field)
            elif issubclass(type(field), Struct):
                sf = StructField(field)
                sf.name = name
                field_defaults[name] = sf.default
                fields.append(sf)
                attrs[name] = sf
        fields.sort(key=lambda x:x.index)
        new_cls = type.__new__(cls, cls_name, bases, attrs)
        new_cls.field_defaults = field_defaults
        new_cls.__FIELDS__ = fields
        return new_cls

class Struct(object, Struct):
    __metaclass__ = StructMeta

    def __init__(self, initial=None):
        self.index = __nextfield__()
        self.field_items = copy.deepcopy(self.field_defaults)
        for field in self.__FIELDS__:
            for linked in field.linked_fields:
                linked.owner = self
        if initial:
            self.unpack(initial)

    def __repr__(self):
        fields = [repr(getattr(self, field.name)) for field in self.__FIELDS__]
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
