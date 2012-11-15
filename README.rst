natsort
=======

Natural sorting for python

Synopsis
--------

The ``natsort`` package provides a key helps sorts lists "naturally"; that is
it sorts alphabetically and numerically, and not by ASCII.  It provides support
for ints and floats (including negatives and exponental notation) and basic
support for sorting version numbers (1.2.3, no letters).

``natsort`` is not necessarily optimized for speed, but it is designed to be as
flexible as possible.

API
---

The ``natsort`` package provides three functions: ``natsort_key``,
``natsorted``, and ``index_natsorted``.

natsort_key
'''''''''''

Using ``natsort_key`` is just like any other sorting key in python:

    >>> from natsort import natsort_key
    >>> a = ['num3', 'num5', 'num2']
    >>> a.sort(key=natsort_key)
    >>> a
    ['num2', 'num3', 'num5']
