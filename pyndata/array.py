from __future__ import absolute_import

from .field import Field
from .structure import Struct
from .structure import StructField
from .variablelength import VariableLength

class array(VariableLength, Field):
    def __init__(self, kind, length):
        super(array, self).__init__()
        
        if issubclass(type(kind), Struct):
            kind = StructField(kind)
        self.kind = kind

        self.length = length

        self.default = []

    def pack(self, values, struct):
        return ''.join(self.kind.pack(item, struct) for item in values)

    def unpack(self, reader, struct):
        out = []
        for x in xrange(self.get_length(struct)):
            out.append(self.kind.unpack(reader, struct))
        return out
