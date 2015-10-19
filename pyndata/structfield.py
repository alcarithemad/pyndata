from __future__ import absolute_import

from .field import Field

class StructField(Field):
    
    def __init__(self, struct):
        self.__DEFAULT__ = struct
        super(StructField, self).__init__()
        self.index = struct.index
        self.struct = type(struct)

    def pack(self, value, struct):
        return value.pack()

    def unpack(self, reader, struct):
        return self.struct(reader)