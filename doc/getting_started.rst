Getting Started
===============

What is this?
-------------

Pyndata is a library to make defining and working with C-style structures easy.

Why?
----

The stdlib module :mod:`struct` just doesn't cut it for complex datastructures and protocols. I don't like the way Construct feels. Suitcase didn't exist when I started, and has some design decisions I disagree with.

Installation
------------

TKTK

Compatibility
-------------

These versions of Python are supported. The test suite is run and passes with both of them.

* Python 2.7
* Python 3.5

Defining a struct
-----------------

.. currentmodule:: pyndata

To create a useful struct, just subclass :class:`Struct` and add some :class:`Field` objects to it.

.. literalinclude:: ../examples/simple.py
    :language: python
