import pyndata

class BytestringTests(pyndata.Struct):
    str1 = pyndata.bytestring(4)

def test_bytestring():
    t = BytestringTests()
    t.str1 = 'asdf'
    assert t.str1 == 'asdf'
    assert t.pack() == 'asdf'
