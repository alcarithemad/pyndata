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

# TODO: VariableArrayTests
