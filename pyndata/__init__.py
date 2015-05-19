import copy
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

class padding(Field):
    def __init__(self, length):
        super(padding, self).__init__()
        self.length = length
        self.default = '\0'*length

    def pack(self, value):
        return '\0'*self.length

    def unpack(self, reader):
        return reader.read(self.length)

class array(Field):
    def __init__(self, kind, length, max_length=None, padded=False):
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
    def __init__(self, max_length, padded=False, allow_max=False):
        super(null_string, self).__init__()
        self.max_length = max_length
        self.padded = padded
        self.default = ''
        self.allow_max = allow_max

    def pack(self, value):
        if self.allow_max:
            if len(value) > self.max_length:
                raise ValueError
        else:
            if len(value) >= self.max_length:
                raise ValueError
        value = (value+'\0')[:self.max_length]
        if self.padded:
            pad = self.max_length - len(value)
            value += '\0'*pad
        return value

    def unpack(self, reader):
        if self.padded:
            value = reader.read(self.max_length)
        else:
            value = ['']
            i = 0
            m = self.max_length + (1 if self.allow_max else 0)
            while value[-1] != '\0' and i < m:
                value.append(reader.read(1))
                i += 1
            value = ''.join(value)
        value = value.rstrip('\0')
        return value

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

class StructField(Field):
    
    def __init__(self, struct_):
        self.__DEFAULT__ = struct_
        super(StructField, self).__init__()
        self.index = struct_.index
        self.struct = type(struct_)

    def __get__(self, obj, kind=None):
        return obj.field_items[self.name]

    def pack(self, value):
        return value.pack()

    def unpack(self, reader):
        return self.struct(reader)

class Struct:
    pass

class StructMeta(type):
    def __new__(cls, cls_name, bases, attrs):
        fields = []
        field_defaults = {}
        for name, field in attrs.items():
            if issubclass(type(field), Field):
                field.name = name
                field_defaults[name] = field.default
                fields.append(field)
            elif issubclass(type(field), Struct):
                sf = StructField(field)
                sf.name = name
                field_defaults[name] = sf.default
                fields.append(sf)
                attrs[name] = sf
        fields.sort(key=lambda x:x.index)
        new_cls = type.__new__(cls, cls_name, bases, attrs)
        new_cls.field_defaults = field_defaults
        new_cls.__FIELDS__ = fields
        return new_cls

class Struct(object, Struct):
    __metaclass__ = StructMeta

    def __init__(self, initial=None):
        self.index = __nextfield__()
        self.field_items = copy.deepcopy(self.field_defaults)
        if initial:
            self.unpack(initial)

    def __repr__(self):
        fields = [repr(getattr(self, field.name)) for field in self.__FIELDS__]
        ret = '{0}({1})'.format(type(self).__name__, ', '.join(fields))
        return ret

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

