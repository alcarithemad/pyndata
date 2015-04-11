import itertools
import struct

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

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
        print 'obj', obj, id(obj)
        return obj.field_items[self.name]

    def __set__(self, obj, value):
        print 'obj', obj, id(obj)
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
        super(Padding, self).__init__()
        self.length = length
        self.default = '\0'*length

    def pack(self, value):
        return '\0'*self.length

    def unpack(self, reader):
        return reader.read(self.length)

class array(Field):
    def __init__(self, kind, length):
        super(array, self).__init__()
        self.kind = kind
        if isinstance(length, int):
            self.length = lambda: length
        else:
            self.length = length
        self.default = [kind.default for x in xrange(self.length())]

    def pack(self, values):
        return ''.join(self.kind.pack(item) for item in values)

    def unpack(self, reader):
        out = []
        for x in xrange(self.length()):
            out.append(self.kind.unpack(reader))
        return out

class null_string(Field):
    def __init__(self, maxlength, padded=False, allow_max=False):
        super(null_string, self).__init__()
        self.maxlength = maxlength
        self.padded = padded
        self.default = ''
        self.allow_max = allow_max

    def pack(self, value):
        if self.allow_max:
            if len(value) > self.maxlength:
                raise ValueError
        else:
            if len(value) >= self.maxlength:
                raise ValueError
        value = (value+'\0')[:self.maxlength]
        if self.padded:
            pad = self.maxlength - len(value)
            value += '\0'*pad
        return value

    def unpack(self, reader):
        if self.padded:
            value = reader.read(self.maxlength)
        else:
            value = ['']
            i = 0
            m = self.maxlength + (1 if self.allow_max else 0)
            while value[-1] != '\0' and i < m:
                value.append(reader.read(1))
                i += 1
            value = ''.join(value)
        value = value.rstrip('\0')
        print 'value', repr(value)
        return value

class StructMeta(type):
    def __new__(cls, name, bases, attrs):
        __FIELDS__ = []
        field_defaults = {}
        for name, field in attrs.items():
            if issubclass(type(field), Field):
                field.name = name
                field_defaults[name] = field.default
                __FIELDS__.append(field)

        __FIELDS__.sort(key=lambda x:x.index)
        attrs['field_defaults'] = field_defaults
        attrs['__FIELDS__'] = __FIELDS__
        new_cls = type.__new__(cls, name, bases, attrs)
        return new_cls

class Struct(object):
    __metaclass__ = StructMeta

    def __init__(self, initial=None):
        self.field_items = {}
        self.field_items.update(self.field_defaults)
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

