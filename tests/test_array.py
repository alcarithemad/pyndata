import pytest

import pyndata

class FixedArrayTests(pyndata.Struct):
    arr = pyndata.array(pyndata.uint8(), 3)

def test_array_unpack():
    x = FixedArrayTests()
    x.unpack(b'\x01\x02\x03')
    assert x.arr == [1,2,3]

def test_array_pack():
    x = FixedArrayTests()
    x.arr = [4,5,6]
    packed = x.pack()
    assert packed == b'\x04\x05\x06'

class S1(pyndata.Struct):
	f = pyndata.uint8()

class S2(pyndata.Struct):
	a = pyndata.array(kind=S1(), length=2)

class VariableArray(pyndata.Struct):
    l = pyndata.uint8()
    a = pyndata.array(pyndata.uint8(), length=l)

def test_variable_unpack_length():
    v = VariableArray()
    v.unpack(b'\x03\x01\x02\x03')
    assert v.l == 3
    assert v.a == [1, 2, 3]

def test_variable_pack():
    v = VariableArray()
    v.a = [1, 2, 3]
    assert v.pack() == b'\x03\x01\x02\x03'

def test_bad_unpack_length():
    v = VariableArray()
    with pytest.raises(pyndata.error):
        v.unpack(b'\x04\x01\x02\x03')

class ArrayWithBitfieldLength(pyndata.Struct):
    a = pyndata.uint8()
    b = pyndata.BitField(a, 8, 0)
    c = pyndata.array(pyndata.uint8(), length=b)

def test_array_bitfield_length():
    x = ArrayWithBitfieldLength(b'\x02\x00\x01')
    assert x.c == [0, 1]
    y = ArrayWithBitfieldLength()
    y.b = 2
    y.c = [0, 1]
    assert y.pack() == b'\x02\x00\x01'

