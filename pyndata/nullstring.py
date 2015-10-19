from __future__ import absolute_import

from .field import Field

class nullstring(Field):
    def __init__(self, max_length, padded=False, allow_max=False):
        super(nullstring, self).__init__()
        self.max_length = max_length
        self.padded = padded
        self.default = ''
        self.allow_max = allow_max

    def pack(self, value, struct):
        if self.allow_max:
            if len(value) > self.max_length:
                raise ValueError("String length {} exceeds this field's maximum length {}".format(len(value), self.max_length))
        else:
            if len(value) >= self.max_length:
                raise ValueError("String length {} exceeds this field's maximum length {}".format(len(value), self.max_length))
        value = (value+'\0')[:self.max_length]
        if self.padded:
            pad = self.max_length - len(value)
            value += '\0'*pad
        return value

    def unpack(self, reader, struct):
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
