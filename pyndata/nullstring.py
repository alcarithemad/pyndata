from __future__ import absolute_import

from .field import Field

class nullstring(Field):
    '''A null-terminated string.
    If padded is True, always reads max_length bytes, and discards everything
    after the first null byte in the result.
    If allow_max is true, and the string is max_length bytes long, it will not
    be required to contain a trailing null byte (e.g., 'asdf' is a valid 
    max_length=4 string, but only if allow_max=True).

    Parameters
        max_length (int): ...

    Keyword Arguments
        padded (bool): ...
        allow_max (bool): ...
    '''
    def __init__(self, max_length, padded=False, allow_max=False):
        super(nullstring, self).__init__()
        self.max_length = max_length
        self.padded = padded
        self.default = ''
        self.allow_max = allow_max

    def pack(self, value, struct):
        if isinstance(value, str):
            value = value.encode('utf-8')
        if self.allow_max:
            if len(value) > self.max_length:
                raise ValueError("String length {} exceeds this field's maximum length {}".format(len(value), self.max_length))
        else:
            if len(value) >= self.max_length:
                raise ValueError("String length {} exceeds this field's maximum length {}".format(len(value), self.max_length))
        value = (value+b'\0')[:self.max_length]
        if self.padded:
            pad = self.max_length - len(value)
            value += b'\0'*pad
        return value

    def unpack(self, reader, struct):
        if self.padded:
            value = reader.read(self.max_length)
        else:
            value = [b'']
            i = 0
            m = self.max_length + (1 if self.allow_max else 0)
            while value[-1] != '\0' and i < m:
                value.append(reader.read(1))
                i += 1
            print(value)
            value = b''.join(value)
        value = value.rstrip(b'\0').decode('utf-8')
        return value
