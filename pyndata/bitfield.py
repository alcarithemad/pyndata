from __future__ import absolute_import

from .field import __nextfield__

class BitField(object):
    default = 0
    __SHOW__ = True
    def __init__(self, field, size, shift=None, enum=None):
        if shift == None:
            shift = field.current_offset
            field.current_offset += size
        self.index = __nextfield__()
        self.field = field
        self.mask = ((1 << size)-1) << shift
        self.shift = shift
        self.enum = enum

    def __get__(self, obj, kind=None):
        value = self.field.__get__(obj)
        value = (value & self.mask) >> self.shift
        try:
            return self.enum(value)
        except:
            return value

    def __set__(self, obj, value):
        value = int(value)
        result = self.field.__get__(obj) & ((~self.mask)&((1<<64)-1))
        result |= ((value << self.shift) & self.mask)
        self.field.__set__(obj, result)
