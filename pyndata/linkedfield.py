from __future__ import absolute_import

from .field import Field
from .structfield import StructField
from .structure import Struct

class LinkedField(object):

    def __init__(self, field):
        if issubclass(type(field), Struct):
            field = StructField(field)
        self.field = [field] # hack to avoid invoking the descriptor on the LinkedField
        self.owner = None # will be set by Struct.__init__

    def __call__(self):
        return self.field[0].__get__(self.owner)

    def set(self, value):
        self.field[0].__set__(self.owner, value)
