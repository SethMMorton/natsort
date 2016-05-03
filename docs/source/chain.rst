.. default-domain:: py
.. currentmodule:: natsort

.. _function_help:

Help With Creating Function Keys
================================

If you need to create a complicated *key* argument to (for example)
:func:`natsorted` that is actually multiple functions called one after the other,
the following function can help you easily perform this action. It is
used internally to :mod:`natsort`, and has been exposed publically for
the convenience of the user.

.. autofunction:: chain_functions

