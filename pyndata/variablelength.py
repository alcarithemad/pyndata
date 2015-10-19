from __future__ import absolute_import

from .field import Field
from .bitfield import BitField

class VariableLength(object):
    def get_length(self, struct):
            if isinstance(self.length, (Field, BitField)):
                return self.length.__get__(struct)
            else:
                return self.length