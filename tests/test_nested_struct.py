import pyndata

class Header(pyndata.Struct):
    msg_len = pyndata.uint8()

class Message(pyndata.Struct):
    hdr = Header()
    s = pyndata.bytestring(length=hdr.msg_len)

def test_nested_reference():
    x = Message()
    x.unpack(b'\x04asdf')
    assert x.hdr.msg_len == 4
    assert x.s == b'asdf'
