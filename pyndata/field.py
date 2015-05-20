from __future__ import absolute_import

import itertools

def __nextfield__():
    return __nextfield__.count.next()
__nextfield__.count = itertools.count()

class Field(object):
    __DEFAULT__ = None

    def __init__(self, default=None):
        self.default = default or self.__DEFAULT__
        self.index = __nextfield__()
        self.name = None

    def __get__(self, obj, kind=None):
        return obj.field_items[self.name]

    def __set__(self, obj, value):
        obj.field_items[self.name] = value

    def pack(self):
        raise NotImplementedError

    def unpack(self, reader):
        raise NotImplementedError
