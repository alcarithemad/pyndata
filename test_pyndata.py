import pytest

import pyndata

class s(pyndata.Struct):
    first = pyndata.uint8()
    second = pyndata.uint8(default=5)

def test_field_get():
    x = s()
    assert x.first == 0

def test_default():
    x = s()
    assert x.second == 5

def test_field_set():
    x = s()
    x.first = 123
    assert x.first == 123

def test_unique_field_items():
    x = s()
    y = s()
    assert id(x.field_items) != id(y.field_items)

def test_pack():
    x = s()
    packed = x.pack()
    assert packed == '\0\x05'

def test_initial_unpack():
    x = s('\x20\xff')
    assert x.first == 0x20
    assert x.second == 0xff

def test_unpack():
    x = s()
    x.unpack('\x31\xf0')
    assert x.first == 0x31
    assert x.second == 0xf0

class padded(pyndata.Struct):
    f = pyndata.uint8(0xff)
    pad = pyndata.Padding(3)

def test_padding_unpack():
    x = padded()
    packed = x.pack()
    assert packed == '\xff\0\0\0'

def test_padding_pack():
    x = padded()
    x.unpack('\x20\x01\x02\x03')
    assert x.pad == '\x01\x02\x03'

class FixedArrayTests(pyndata.Struct):
    arr = pyndata.array(pyndata.uint8(), 3)

def test_array_unpack():
    x = FixedArrayTests()
    x.unpack('\x01\x02\x03')
    assert x.arr == [1,2,3]

def test_array_pack():
    x = FixedArrayTests()
    x.arr = [4,5,6]
    packed = x.pack()
    assert packed == '\x04\x05\x06'

# TODO: VariableArrayTests

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

class SubStruct(pyndata.Struct):
    x = pyndata.uint8()

print '1', SubStruct
print '2', SubStruct()

class StructWithSubStruct(pyndata.Struct):
    s1 = SubStruct()
    print s1
    s2 = SubStruct()

def test_sub_struct():
    t = StructWithSubStruct('\xff\xcc')
    print StructWithSubStruct.s1
    print 'it', t.field_items
    print 'dt', t.field_defaults
    print 'in test', hex(id(t.s1))
    assert t.s1.x == 0xff
    assert t.s2.x == 0xcc
