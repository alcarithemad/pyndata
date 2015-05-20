from __future__ import absolute_import

from .field import Field

class StructField(Field):
    
    def __init__(self, struct_):
        self.__DEFAULT__ = struct_
        super(StructField, self).__init__()
        self.index = struct_.index
        self.struct = type(struct_)

    def __get__(self, obj, kind=None):
        return obj.field_items[self.name]

    def pack(self, value):
        return value.pack()

    def unpack(self, reader):
        return self.struct(reader)