.. default-domain:: py
.. currentmodule:: natsort

.. _api:

natsort API
===========

.. contents::
    :local:

Standard API
------------

:func:`~natsort.natsorted`
++++++++++++++++++++++++++

.. autofunction:: natsorted

The :class:`~natsort.ns` enum
+++++++++++++++++++++++++++++

.. autodata:: ns
    :annotation:

:func:`~natsort.natsort_key`
++++++++++++++++++++++++++++

.. autofunction:: natsort_key

:func:`~natsort.natsort_keygen`
+++++++++++++++++++++++++++++++

.. autofunction:: natsort_keygen

:func:`~natsort.os_sort_key`
++++++++++++++++++++++++++++

.. autofunction:: os_sort_key

:func:`~natsort.os_sort_keygen`
+++++++++++++++++++++++++++++++

.. autofunction:: os_sort_keygen

Convenience Functions
---------------------

:func:`~natsort.os_sorted`
+++++++++++++++++++++++++++

.. autofunction:: os_sorted

:func:`~natsort.realsorted`
+++++++++++++++++++++++++++

.. autofunction:: realsorted

:func:`~natsort.humansorted`
++++++++++++++++++++++++++++

.. autofunction:: humansorted

:func:`~natsort.index_natsorted`
++++++++++++++++++++++++++++++++

.. autofunction:: index_natsorted

:func:`~natsort.index_realsorted`
+++++++++++++++++++++++++++++++++

.. autofunction:: index_realsorted

:func:`~natsort.index_humansorted`
++++++++++++++++++++++++++++++++++

.. autofunction:: index_humansorted

:func:`~natsort.order_by_index`
+++++++++++++++++++++++++++++++

.. autofunction:: order_by_index

.. _bytes_help:

Help With Bytes
+++++++++++++++

The official stance of :mod:`natsort` is to not support `bytes` for
sorting; there is just too much that can go wrong when trying to automate
conversion between `bytes` and `str`. But rather than completely give up
on `bytes`, :mod:`natsort` provides three functions that make it easy to
quickly decode `bytes` to `str` so that sorting is possible.

.. autofunction:: decoder

.. autofunction:: as_ascii

.. autofunction:: as_utf8

.. _function_help:

Help With Creating Function Keys
++++++++++++++++++++++++++++++++

If you need to create a complicated *key* argument to (for example)
:func:`natsorted` that is actually multiple functions called one after the
other, the following function can help you easily perform this action. It is
used internally to :mod:`natsort`, and has been exposed publicly for
the convenience of the user.

.. autofunction:: chain_functions

If you need to be able to search your input for numbers using the same
definition as :mod:`natsort`, you can do so using the following function.
Given your chosen algorithm (selected using the :class:`~natsort.ns` enum),
the corresponding regular expression to locate numbers will be returned.

.. autofunction:: numeric_regex_chooser

Help With Type Hinting
++++++++++++++++++++++

If you need to explicitly specify the types that natsort accepts or returns
in your code, the following types have been exposed for your convenience.

+--------------------------------+----------------------------------------------------------------------------------------+
| Type                           | Purpose                                                                                |
+================================+========================================================================================+
|:attr:`natsort.NatsortKeyType`  | Returned by :func:`natsort.natsort_keygen`, and type of :attr:`natsort.natsort_key`    |
+--------------------------------+----------------------------------------------------------------------------------------+
|:attr:`natsort.OSSortKeyType`   | Returned by :func:`natsort.os_sort_keygen`, and type of :attr:`natsort.os_sort_key`    |
+--------------------------------+----------------------------------------------------------------------------------------+
|:attr:`natsort.KeyType`         | Type of `key` argument to :func:`natsort.natsorted` and :func:`natsort.natsort_keygen` |
+--------------------------------+----------------------------------------------------------------------------------------+
|:attr:`natsort.NatsortInType`   | The input type of :attr:`natsort.NatsortKeyType`                                       |
+--------------------------------+----------------------------------------------------------------------------------------+
|:attr:`natsort.NatsortOutType`  | The output type of :attr:`natsort.NatsortKeyType`                                      |
+--------------------------------+----------------------------------------------------------------------------------------+
|:attr:`natsort.NSType`          | The type of the :class:`ns` enum                                                       |
+--------------------------------+----------------------------------------------------------------------------------------+
