import pyndata

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