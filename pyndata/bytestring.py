from __future__ import absolute_import

from .error import error
from .field import Field
from .variablelength import VariableLength

class bytestring(VariableLength, Field):
    '''Like array, but unpacked as a python string of arbitrary data.
    '''
    def __init__(self, length):
        super(bytestring, self).__init__()
        self.length = length
        self.default = ''

    def pack(self, value, struct):
        return value

    def unpack(self, reader, struct):
        l = self.get_length(struct)
        data = reader.read(l)
        if len(data) != l:
            raise error("Not enough bytes, expected {}, got {}".format(l, repr(data)))
        else:
            return data
