from __future__ import absolute_import

from .field import Field

class padding(Field):
    def __init__(self, length):
        super(padding, self).__init__()
        self.length = length
        self.default = '\0'*length

    def pack(self, value):
        return '\0'*self.length

    def unpack(self, reader):
        return reader.read(self.length)
