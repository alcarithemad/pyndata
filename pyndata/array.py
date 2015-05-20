from __future__ import absolute_import

from .field import Field
from .structure import Struct
from .structure import StructField

class array(Field):
    def __init__(self, kind, length, padded=False):
        super(array, self).__init__()
        if issubclass(type(kind), Struct):
            kind = StructField(kind)    
        self.kind = kind
        if isinstance(length, int):
            self.length = lambda: length
        else:
            self.length = length
        self.default = [kind.default for x in xrange(self.length())]

    def pack(self, values):
        return ''.join(self.kind.pack(item) for item in values)

    def unpack(self, reader):
        out = []
        for x in xrange(self.length()):
            out.append(self.kind.unpack(reader))
        return out