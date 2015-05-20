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
