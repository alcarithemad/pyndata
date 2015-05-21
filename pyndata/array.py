from __future__ import absolute_import

from .field import Field
from .structure import Struct
from .structure import StructField
from .varlen import VariableLength

class array(VariableLength, Field):
    def __init__(self, kind, length):
        super(array, self).__init__(length)
        
        if issubclass(type(kind), Struct):
            kind = StructField(kind)
        self.kind = kind

        self.default = []

    def pack(self, values):
        return ''.join(self.kind.pack(item) for item in values)

    def unpack(self, reader):
        out = []
        print self.length
        for x in xrange(self.length()):
            out.append(self.kind.unpack(reader))
        return out
