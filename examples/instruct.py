import pyndata

class Header(pyndata.Struct):
    msg_type = pyndata.uint8()

class Message(pyndata.Struct):
    hdr = Header()
    
