from __future__ import absolute_import

from .field import Field
from .bitfield import BitField

class VariableLength(object):
    def get_length(self, struct):
            if isinstance(self.length, (Field, BitField)):
                return self.length.__get__(struct)
            else:
                return self.length

    def __set__(self, obj, value):
        super(VariableLength, self).__set__(obj, value)
        if isinstance(self.length, (Field, BitField)):
            return self.length.__set__(obj, len(value))
