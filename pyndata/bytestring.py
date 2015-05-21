from __future__ import absolute_import

from .field import Field
from .varlen import VariableLength

class bytestring(VariableLength, Field):
    def __init__(self, length):
        super(bytestring, self).__init__(length)
        self.default = ''

    def pack(self, value):
        return value

    def unpack(self, reader):
        return reader.read(self.length())