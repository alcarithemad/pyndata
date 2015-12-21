from __future__ import absolute_import

import struct

from .field import Field
from .error import error

class integer(Field):
    '''A binary packed integer type. This is implemented with the Python stdlib :mod:`struct` module.
    Subclass it and set __TYPE__ on the subclass to a :mod:`struct` type code.
    '''
    __TYPE__ = 'b'
    __DEFAULT__ = 0
    __ENDIAN__ = None

    def __init__(self, endian=None, enum=None, *args, **kwargs):
        super(integer, self).__init__(*args, **kwargs)
        self.__ENDIAN__ = endian
        self.enum = enum
        self.current_offset = 0 # for bitfields

    def endian(self, _struct):
        return '>' if (self.__ENDIAN__ or _struct.__ENDIAN__) == 'big' else '<'

    def pack(self, value, _struct):
        value = int(value)
        return struct.pack(self.endian(_struct)+self.__TYPE__, value)

    def unpack(self, reader, _struct):
        size = struct.calcsize(self.endian(_struct)+self.__TYPE__)
        data = reader.read(size)
        if len(data) != size:
            raise error("Not enough bytes, expected {}, got {}".format(size, repr(data)))
        value = struct.unpack(self.endian(_struct)+self.__TYPE__, data)[0]
        try:
            return self.enum(value)
        except:
            return value

class int8(integer): __TYPE__ = 'b'
class int16(integer): __TYPE__ = 'h'
class int32(integer): __TYPE__ = 'i'
class int64(integer): __TYPE__ = 'q'

class uint8(integer): __TYPE__ = 'B'
class uint16(integer): __TYPE__ = 'H'
class uint32(integer): __TYPE__ = 'I'
class uint64(integer): __TYPE__ = 'Q'

__all__ = [
    'integer',
    'int8',
    'int16',
    'int32',
    'int64',
    'uint8',
    'uint16',
    'uint32',
    'uint64'
]