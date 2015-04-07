.. default-domain:: py
.. currentmodule:: natsort

.. _bytes_help:

Help With Bytes On Python 3
===========================

The official stance of :mod:`natsort` is to not support `bytes` for
sorting; there is just too much that can go wrong when trying to automate
conversion between `bytes` and `str`. But rather than completely give up
on `bytes`, :mod:`natsort` provides three functions that make it easy to
quickly decode `bytes` to `str` so that sorting is possible.

.. autofunction:: decoder

.. autofunction:: as_ascii

.. autofunction:: as_utf8

