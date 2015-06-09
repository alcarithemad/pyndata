from __future__ import absolute_import

from .field import Field

class VariableLength(object):
    def get_length(self, struct):
            if isinstance(self.length, Field):
                return struct.field_items[self.length.name]
            else:
                return self.length
