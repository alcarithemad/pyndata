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
    pad = pyndata.padding(3)

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

class StructWithSubStruct(pyndata.Struct):
    s1 = SubStruct()
    s2 = SubStruct()

def test_sub_struct_unpack():
    t = StructWithSubStruct('\xff\xcc')
    assert t.s1.x == 0xff
    assert t.s2.x == 0xcc

def test_sub_struct_pack():
    t = StructWithSubStruct()
    t.s1.x = 0x20
    t.s2.x = 0x44
    packed = t.pack()
    assert packed == '\x20\x44'

class BitFieldTests(pyndata.Struct):
    real = pyndata.uint16()
    bit1 = pyndata.BitField(real, 4, 0)
    bit2 = pyndata.BitField(real, 1, 4)
    bit3 = pyndata.BitField(real, 3, 5)
    bit4 = pyndata.BitField(real, 8, 8)

def test_bitfield():
    b = BitFieldTests()
    b.bit1 = 3
    b.bit2 = 1
    b.bit3 = 6
    b.bit4 = 0b10101010
    assert b.bit1 == 3
    assert b.bit2 == 1
    assert b.bit3 == 6
    assert b.bit4 == 0b10101010

class BytestringTests(pyndata.Struct):
    str1 = pyndata.bytestring(4)

def test_bytestring():
    t = BytestringTests()
    t.str1 = 'asdf'
    assert t.str1 == 'asdf'
    assert t.pack() == 'asdf'

