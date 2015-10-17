import pytest

import pyndata

class S(pyndata.Struct):
	_a = pyndata.uint8()
	b = pyndata.uint8()

def test_default_hidden():
	x = S()
	a = repr(x)
	assert a == "S(b=0)"
