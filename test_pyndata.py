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

class FixedArrayExample(pyndata.Struct):
    arr = pyndata.array(pyndata.uint8(), 3)

def test_array_unpack():
    x = FixedArrayExample()
    x.unpack('\x01\x02\x03')
    assert x.arr == [1,2,3]

def test_array_pack():
    x = FixedArrayExample()
    x.arr = [4,5,6]
    packed = x.pack()
    assert packed == '\x04\x05\x06'

# TODO: VariableArrayExample
