import pyndata

class BytestringTests(pyndata.Struct):
    str1 = pyndata.bytestring(4)

def test_bytestring():
    t = BytestringTests()
    t.str1 = 'asdf'
    assert t.str1 == 'asdf'
    assert t.pack() == 'asdf'

class VariableBytestring(pyndata.Struct):
	l = pyndata.uint8()
	s = pyndata.bytestring(length=l)

def test_variable_unpack():
	v = VariableBytestring()
	v.unpack('\x04asdf')
	assert v.l == 4
	assert v.s == 'asdf'
