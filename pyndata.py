import itertools
import struct

try:
    from cStringIO import StringIO
except:
    import StringIO

def __nextfield__():
    return __nextfield__.count.next()
__nextfield__.count = itertools.count()

# TODO: endianness

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
        raise NotImplemented

    def unpack(self, reader):
        raise NotImplemented

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

class Padding(Field):
    def __init__(self, length):
        self.length = length
        self.default = '\0'*length

    def pack(self, value):
        return '\0'*self.length

    def unpack(self, reader):
        return reader.read(self.length)

class array(Field):
    pass

class StructMeta(type):
    def __new__(cls, name, bases, attrs):
        __FIELDS__ = []
        field_items = {}
        for name, field in attrs.items():
            if issubclass(type(field), Field):
                field.name = name
                field_items[name] = field.default
                __FIELDS__.append(field)

        __FIELDS__.sort(key=lambda x:x.index)
        attrs['field_items'] = field_items
        attrs['__FIELDS__'] = __FIELDS__
        new_cls = type.__new__(cls, name, bases, attrs)
        return new_cls

class Struct(object):
    __metaclass__ = StructMeta

    def __init__(self, initial=None):
        if initial:
            self.unpack(initial)

    def pack(self):
        out = []
        for field in self.__FIELDS__:
            out.append(field.pack(self.field_items[field.name]))
        return ''.join(out)

    def unpack(self, reader):
        if isinstance(reader, str):
            reader = StringIO(reader)
        for field in self.__FIELDS__:
            self.field_items[field.name] = field.unpack(reader)

if __name__ == '__main__':
    s = Struct()
    print s

    class Foo(Struct):
        first = int16()
        second = uint64(default=32)

    print 'f', Foo
    print Foo.__FIELDS__
    f = Foo('\xff'*10)
    f.first = 5
    print f.first, f.second
    print f.field_items
