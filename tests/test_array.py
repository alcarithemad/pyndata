import pytest

import pyndata

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

class S1(pyndata.Struct):
	f = pyndata.uint8()

class S2(pyndata.Struct):
	a = pyndata.array(kind=S1(), length=2)

class VariableArray(pyndata.Struct):
    l = pyndata.uint8()
    a = pyndata.array(pyndata.uint8(), length=l)

def test_variable_unpack_length():
    v = VariableArray()
    v.unpack('\x03\x01\x02\x03')
    assert v.l == 3
    assert v.a == [1, 2, 3]

def test_bad_unpack_length():
    v = VariableArray()
    with pytest.raises(pyndata.error):
        v.unpack('\x04\x01\x02\x03')
