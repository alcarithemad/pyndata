import pyndata

class BitFieldTests(pyndata.Struct):
    real = pyndata.uint16()
    bit1 = pyndata.BitField(real, 4, 0)
    bit2 = pyndata.BitField(real, 1, 4)
    bit3 = pyndata.BitField(real, 3, 5)
    bit4 = pyndata.BitField(real, 8, 8)

def test_bitfield():
    b = BitFieldTests()
    b.bit1 = 3
    b.bit2 = 1
    b.bit3 = 6
    b.bit4 = 0b10101010
    assert b.bit1 == 3
    assert b.bit2 == 1
    assert b.bit3 == 6
    assert b.bit4 == 0b10101010
