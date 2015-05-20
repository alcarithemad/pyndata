import pytest

import pyndata

class NullStringTests(pyndata.Struct):
    str1 = pyndata.null_string(max_length=4)
    str2 = pyndata.null_string(max_length=4, padded=True)
    str3 = pyndata.null_string(max_length=4, allow_max=True)

def test_null_string_pack():
    x = NullStringTests()
    packed = x.pack()
    assert packed == '\0\0\0\0\0\0'

def test_null_string_illegal():
    x = NullStringTests()
    x.str1 = 'asdf'
    with pytest.raises(ValueError):
        x.pack()

def test_null_string_illegal_allow_max():
    x = NullStringTests()
    x.str3 = 'asdfg'
    with pytest.raises(ValueError):
        x.pack()

def test_null_string_unpack():
    x = NullStringTests()
    x.unpack('asd\x00as\x00\x001234')
    assert x.str1 == 'asd'
    assert x.str2 == 'as'
    assert x.str3 == '1234'
