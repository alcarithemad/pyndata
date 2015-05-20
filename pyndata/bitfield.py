from __future__ import absolute_import

from .field import __nextfield__

class BitField(object):
    default = 0
    SHOW = True
    def __init__(self, field, size, shift):
        self.index = __nextfield__()
        self.field = field
        self.mask = ((1 << size)-1) << shift
        self.shift = shift

    def __get__(self, obj, kind=None):
        value = self.field.__get__(obj)
        return (value & self.mask) >> self.shift

    def __set__(self, obj, value):
        result = self.field.__get__(obj) & ((~self.mask)&((1<<64)-1))
        result |= ((value << self.shift) & self.mask)
        self.field.__set__(obj, result)