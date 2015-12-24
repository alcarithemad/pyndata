import pyndata

class Message(pyndata.Struct):
    msg_type = pyndata.uint8()
    msg_length = pyndata.uint16(endian='big')
    payload = pyndata.bytestring(length=msg_length)

m = Message()
m.msg_type = 1
m.payload = b'asdf'

print(repr(m.pack())) # '\x01\x00\x04asdf'
