from __future__ import absolute_import

import itertools

# The basic premise of this whole pile of magic is right here.
# When we __init__ a field we grab a unique index value for it
# we use __nextfield__ for that: it's a little odd, but it's just
# a reference to an otherwise anonymous itertools.count(). This
# would probably be more idiomatic as a class with a __call__, though.
__nextfield__ = itertools.count().next

class Field(object):
    __DEFAULT__ = None
    __SHOW__ = True

    def __init__(self, default=None):
        self.default = default or self.__DEFAULT__
        self.index = __nextfield__()
        self.name = None

    def __get__(self, obj, kind=None):
        return obj.field_items[self.name]

    def __set__(self, obj, value):
        obj.field_items[self.name] = value

    def pack(self, value, struct):
        raise NotImplementedError

    def unpack(self, reader, struct):
        raise NotImplementedError
