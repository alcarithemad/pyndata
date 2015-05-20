import pyndata

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
