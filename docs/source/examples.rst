.. default-domain:: py
.. currentmodule:: natsort

.. _examples:

Examples and Recipes
====================

If you want more detailed examples than given on this page, please see
https://github.com/SethMMorton/natsort/tree/master/test_natsort.

Basic Usage
-----------

In the most basic use case, simply import :func:`~natsorted` and use
it as you would :func:`sorted`::

    >>> a = ['a50', 'a51.', 'a50.4', 'a5.034e1', 'a50.300']
    >>> sorted(a)
    ['a5.034e1', 'a50', 'a50.300', 'a50.4', 'a51.']
    >>> from natsort import natsorted
    >>> natsorted(a)
    ['a50', 'a50.300', 'a5.034e1', 'a50.4', 'a51.']

Customizing Float Definition
---------------------------- 

By default :func:`~natsorted` searches for any float that would be
a valid Python float literal, such as 5, 0.4, -4.78, +4.2E-34, etc.
Perhaps you don't want to search for signed numbers, or you don't
want to search for exponential notation, and the ``signed`` and
``exp`` options allow you to do this::

    >>> a = ['a50', 'a51.', 'a+50.4', 'a5.034e1', 'a+50.300']
    >>> natsorted(a)
    ['a50', 'a+50.300', 'a5.034e1', 'a+50.4', 'a51.']
    >>> natsorted(a, signed=False)
    ['a50', 'a5.034e1', 'a51.', 'a+50.300', 'a+50.4']
    >>> natsorted(a, exp=False)
    ['a5.034e1', 'a50', 'a+50.300', 'a+50.4', 'a51.']

Sort Version Numbers
--------------------

With default options, :func:`~natsorted` will not sort version numbers
well. Version numbers are best sorted by searching for valid unsigned int
literals, not floats.  This can be achieved in three ways, as shown below::

    >>> a = ['ver-2.9.9a', 'ver-1.11', 'ver-2.9.9b', 'ver-1.11.4', 'ver-1.10.1']
    >>> natsorted(a)  # This gives incorrect results
    ['ver-2.9.9a', 'ver-2.9.9b', 'ver-1.11', 'ver-1.11.4', 'ver-1.10.1']
    >>> natsorted(a, number_type=int, signed=False)
    ['ver-1.10.1', 'ver-1.11', 'ver-1.11.4', 'ver-2.9.9a', 'ver-2.9.9b']
    >>> natsorted(a, number_type=None)
    ['ver-1.10.1', 'ver-1.11', 'ver-1.11.4', 'ver-2.9.9a', 'ver-2.9.9b']
    >>> from natsort import versorted
    >>> versorted(a)
    ['ver-1.10.1', 'ver-1.11', 'ver-1.11.4', 'ver-2.9.9a', 'ver-2.9.9b']

You can see that ``number_type=None`` is a shortcut for ``number_type=int``
and ``signed=False``, and the :func:`~versorted` is a shortcut for
``natsorted(number_type=None)``.  The recommend manner to sort version
numbers is to use :func:`~versorted`.

Sorting with Alpha, Beta, and Release Candidates
++++++++++++++++++++++++++++++++++++++++++++++++

By default, if you wish to sort versions with a non-strict versioning
scheme, you may not get the results you expect::

    >>> a = ['1.2', '1.2rc1', '1.2beta2', '1.2beta', '1.2alpha', '1.2.1', '1.1', '1.3']
    >>> versorted(a)
    ['1.1', '1.2', '1.2.1', '1.2alpha', '1.2beta', '1.2beta2', '1.2rc1', '1.3']

To make the '1.2' pre-releases come before '1.2.1', you need to use the following
recipe::

    >>> versorted(a, key=lambda x: x.replace('.', '~'))
    ['1.1', '1.2', '1.2alpha', '1.2beta', '1.2beta2', '1.2rc1', '1.2.1', '1.3']

Please see `this issue <https://github.com/SethMMorton/natsort/issues/13>`_ to
see why this works.

Sort OS-Generated Paths
-----------------------

In some cases when sorting file paths with OS-Generated names, the default
:mod:`~natsorted` algorithm may not be sufficient.  In cases like these,
you may need to use the ``as_path`` option::

    >>> a = ['./folder/file (1).txt',
    ...      './folder/file.txt',
    ...      './folder (1)/file.txt',
    ...      './folder (10)/file.txt']
    >>> natsorted(a)
    ['./folder (1)/file.txt', './folder (10)/file.txt', './folder/file (1).txt', './folder/file.txt']
    >>> natsorted(a, as_path=True)
    ['./folder/file.txt', './folder/file (1).txt', './folder (1)/file.txt', './folder (10)/file.txt']

Using a Custom Sorting Key
--------------------------

Like the built-in ``sorted`` function, ``natsorted`` can accept a custom
sort key so that::

    >>> from operator import attrgetter, itemgetter
    >>> a = [['a', 'num4'], ['b', 'num8'], ['c', 'num2']]
    >>> natsorted(a, key=itemgetter(1))
    [['c', 'num2'], ['a', 'num4'], ['b', 'num8']]
    >>> class Foo:
    ...    def __init__(self, bar):
    ...        self.bar = bar
    ...    def __repr__(self):
    ...        return "Foo('{0}')".format(self.bar)
    >>> b = [Foo('num3'), Foo('num5'), Foo('num2')]
    >>> natsorted(b, key=attrgetter('bar'))
    [Foo('num2'), Foo('num3'), Foo('num5')]

Generating a Natsort Key
------------------------

If you need to sort a list in-place, you cannot use :func:`~natsorted`; you
need to pass a key to the :meth:`list.sort` method. The function
:func:`~natsort_keygen` is a convenient way to generate these keys for you::

    >>> from natsort import natsort_keygen
    >>> a = ['a50', 'a51.', 'a50.4', 'a5.034e1', 'a50.300']
    >>> natsort_key = natsort_keygen()
    >>> a.sort(key=natsort_key)
    >>> a
    ['a50', 'a50.300', 'a5.034e1', 'a50.4', 'a51.']
    >>> versort_key = natsort_keygen(number_type=None)
    >>> a = ['ver-2.9.9a', 'ver-1.11', 'ver-2.9.9b', 'ver-1.11.4', 'ver-1.10.1']
    >>> a.sort(key=versort_key)
    >>> a
    ['ver-1.10.1', 'ver-1.11', 'ver-1.11.4', 'ver-2.9.9a', 'ver-2.9.9b']

:func:`~natsort_keygen` has the same API as :func:`~natsorted`.

Sorting Multiple Lists According to a Single List
-------------------------------------------------

Sometimes you have multiple lists, and you want to sort one of those
lists and reorder the other lists according to how the first was sorted.
To achieve this you would use the :func:`~index_natsorted` or
:func:`~index_versorted` in combination with the convenience function
:func:`~order_by_index`::

    >>> from natsort import index_natsorted, order_by_index
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> b = [4,    5,    6,    7,    8]
    >>> c = ['hi', 'lo', 'ah', 'do', 'up']
    >>> index = index_natsorted(a)
    >>> order_by_index(a, index)
    ['a1', 'a2', 'a4', 'a9', 'a10']
    >>> order_by_index(b, index)
    [6, 4, 7, 5, 8]
    >>> order_by_index(c, index)
    ['ah', 'hi', 'do', 'lo', 'up']

Returning Results in Reverse Order
----------------------------------

Just like the :func:`sorted` built-in function, you can supply the
``reverse`` option to return the results in reverse order::

    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a, reverse=True)
    ['a10', 'a9', 'a4', 'a2', 'a1']
