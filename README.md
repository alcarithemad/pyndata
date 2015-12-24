pyndata - concise struct packing
====

Pyndata is a library for dealing with structured binary data in Python. It's vaguely inspired by the [bindata gem for Ruby](https://github.com/dmendel/bindata).

Features
=====

* Simple, declarative syntax.
* Easily composable.
* Simple bitfield support.
* Variable length fields, e.g. arrays.
* Attach enums to integer fields.

Developing
==========

Pyndata doesn't have any dependencies for regular use, but for development, `enum34` (on 2.x only), `pytest`, and `pytest-cov` are recommended. You can `pip install -r devel-reqs2.txt` to get all of them, or use `devel-reqs3.txt` on Python 3.

Tests
=====

Pyndata uses py.test for unit tests. There's a small collection of unit tests in `tests/`.

