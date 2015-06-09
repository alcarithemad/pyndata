from __future__ import absolute_import

from .field import Field
from .variablelength import VariableLength

class bytestring(VariableLength, Field):
    def __init__(self, length):
        super(bytestring, self).__init__()
        self.length = length
        self.default = ''

    def pack(self, value, struct):
        return value

    def unpack(self, reader, struct):
        return reader.read(self.get_length(struct))
