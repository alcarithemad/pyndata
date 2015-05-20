from __future__ import absolute_import

import struct

from .field import Field

# TODO: endianness

class integer(Field):
    __TYPE__ = 'b'
    __DEFAULT__ = 0

    def pack(self, value):
        return struct.pack(self.__TYPE__, value)

    def unpack(self, reader):
        size = struct.calcsize(self.__TYPE__)
        data = reader.read(size)
        return struct.unpack(self.__TYPE__, data)[0]

class int8(integer): __TYPE__ = 'b'
class int16(integer): __TYPE__ = 'h'
class int32(integer): __TYPE__ = 'i'
class int64(integer): __TYPE__ = 'q'

class uint8(integer): __TYPE__ = 'B'
class uint16(integer): __TYPE__ = 'H'
class uint32(integer): __TYPE__ = 'I'
class uint64(integer): __TYPE__ = 'Q'
