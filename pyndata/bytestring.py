from __future__ import absolute_import

from .field import Field

class bytestring(Field):
    def __init__(self, length):
        super(bytestring, self).__init__()
        if isinstance(length, int):
            self.length = lambda: length
        else:
            self.length = length
        self.default = ''

    def pack(self, value):
        return value

    def unpack(self, reader):
        return reader.read(self.length())