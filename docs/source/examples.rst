.. default-domain:: py
.. currentmodule:: natsort

.. _examples:

Examples and Recipes
====================

If you want more detailed examples than given on this page, please see
https://github.com/SethMMorton/natsort/tree/master/test_natsort.

.. contents::
    :local:

Basic Usage
-----------

In the most basic use case, simply import :func:`~natsorted` and use
it as you would :func:`sorted`:

.. code-block:: python

    >>> a = ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    >>> sorted(a)
    ['1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '2 ft 7 in', '7 ft 6 in']
    >>> from natsort import natsorted, ns
    >>> natsorted(a)
    ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 ft 6 in', '10 ft 2 in']

Sort Version Numbers
--------------------

As of :mod:`natsort` version >= 4.0.0, :func:`~natsorted` will now properly
sort version numbers. The old function :func:`~versorted` exists for
backwards compatibility but new development should use :func:`~natsorted`.

.. _rc_sorting:

Sorting with Alpha, Beta, and Release Candidates
++++++++++++++++++++++++++++++++++++++++++++++++

By default, if you wish to sort versions with a non-strict versioning
scheme, you may not get the results you expect:

.. code-block:: python

    >>> a = ['1.2', '1.2rc1', '1.2beta2', '1.2beta1', '1.2alpha', '1.2.1', '1.1', '1.3']
    >>> natsorted(a)
    ['1.1', '1.2', '1.2.1', '1.2alpha', '1.2beta1', '1.2beta2', '1.2rc1', '1.3']

To make the '1.2' pre-releases come before '1.2.1', you need to use the following
recipe:

.. code-block:: python

    >>> natsorted(a, key=lambda x: x.replace('.', '~'))
    ['1.1', '1.2', '1.2alpha', '1.2beta1', '1.2beta2', '1.2rc1', '1.2.1', '1.3']

If you also want '1.2' after all the alpha, beta, and rc candidates, you can
modify the above recipe:

.. code-block:: python

    >>> natsorted(a, key=lambda x: x.replace('.', '~')+'z')
    ['1.1', '1.2alpha', '1.2beta1', '1.2beta2', '1.2rc1', '1.2', '1.2.1', '1.3']

Please see `this issue <https://github.com/SethMMorton/natsort/issues/13>`_ to
see why this works.

.. _path_sort:

Sort OS-Generated Paths
-----------------------

In some cases when sorting file paths with OS-Generated names, the default
:mod:`~natsorted` algorithm may not be sufficient.  In cases like these,
you may need to use the ``ns.PATH`` option:

.. code-block:: python

    >>> a = ['./folder/file (1).txt',
    ...      './folder/file.txt',
    ...      './folder (1)/file.txt',
    ...      './folder (10)/file.txt']
    >>> natsorted(a)
    ['./folder (1)/file.txt', './folder (10)/file.txt', './folder/file (1).txt', './folder/file.txt']
    >>> natsorted(a, alg=ns.PATH)
    ['./folder/file.txt', './folder/file (1).txt', './folder (1)/file.txt', './folder (10)/file.txt']

Locale-Aware Sorting (Human Sorting)
------------------------------------

.. note:: 
    Please read :ref:`locale_issues` before using ``ns.LOCALE``, :func:`humansorted`,
    or :func:`index_humansorted`.

You can instruct :mod:`natsort` to use locale-aware sorting with the
``ns.LOCALE`` option. In addition to making this understand non-ASCII
characters, it will also properly interpret non-'.' decimal separators
and also properly order case.  It may be more convenient to just use
the :func:`humansorted` function:

.. code-block:: python

    >>> from natsort import humansorted
    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    'en_US.UTF-8'
    >>> a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    >>> natsorted(a, alg=ns.LOCALE)
    ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']
    >>> humansorted(a)
    ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']

You may find that if you do not explicitly set the locale your results may not
be as you expect... I have found that it depends on the system you are on.
If you use `PyICU <https://pypi.org/project/PyICU>`_ (see below) then
you should not need to do this.

.. _case_sort:

Controlling Case When Sorting
-----------------------------

For non-numbers, by default :mod:`natsort` used ordinal sorting (i.e.
it sorts by the character's value in the ASCII table).  For example:

.. code-block:: python

    >>> a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    >>> natsorted(a)
    ['Apple', 'Banana', 'Corn', 'apple', 'banana', 'corn']

There are times when you wish to ignore the case when sorting,
you can easily do this with the ``ns.IGNORECASE`` option:

.. code-block:: python

    >>> natsorted(a, alg=ns.IGNORECASE)
    ['Apple', 'apple', 'Banana', 'banana', 'corn', 'Corn']

Note thats since Python's sorting is stable, the order of equivalent
elements after lowering the case is the same order they appear in the
original list.

Upper-case letters appear first in the ASCII table, but many natural
sorting methods place lower-case first.  To do this, use
``ns.LOWERCASEFIRST``:

.. code-block:: python

    >>> natsorted(a, alg=ns.LOWERCASEFIRST)
    ['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']

It may be undesirable to have the upper-case letters grouped together
and the lower-case letters grouped together; most would expect all
"a"s to bet together regardless of case, and all "b"s, and so on. To
achieve this, use ``ns.GROUPLETTERS``:

.. code-block:: python

    >>> natsorted(a, alg=ns.GROUPLETTERS)
    ['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']

You might combine this with ``ns.LOWERCASEFIRST`` to get what most
would expect to be "natural" sorting:

.. code-block:: python

    >>> natsorted(a, alg=ns.G | ns.LF)
    ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']

Customizing Float Definition
----------------------------

You can make :func:`~natsorted` search for any float that would be
a valid Python float literal, such as 5, 0.4, -4.78, +4.2E-34, etc.
using the ``ns.FLOAT`` key. You can disable the exponential component
of the number with ``ns.NOEXP``.

.. code-block:: python

    >>> a = ['a50', 'a51.', 'a+50.4', 'a5.034e1', 'a+50.300']
    >>> natsorted(a, alg=ns.FLOAT)
    ['a50', 'a5.034e1', 'a51.', 'a+50.300', 'a+50.4']
    >>> natsorted(a, alg=ns.FLOAT | ns.SIGNED)
    ['a50', 'a+50.300', 'a5.034e1', 'a+50.4', 'a51.']
    >>> natsorted(a, alg=ns.FLOAT | ns.SIGNED | ns.NOEXP)
    ['a5.034e1', 'a50', 'a+50.300', 'a+50.4', 'a51.']

For convenience, the ``ns.REAL`` option is provided which is a shortcut
for ``ns.FLOAT | ns.SIGNED`` and can be used to sort on real numbers.
This can be easily accessed with the :func:`~realsorted` convenience
function. Please note that the behavior of the :func:`~realsorted` function
was the default behavior of :func:`~natsorted` for :mod:`natsort`
version < 4.0.0:

.. code-block:: python

    >>> natsorted(a, alg=ns.REAL)
    ['a50', 'a+50.300', 'a5.034e1', 'a+50.4', 'a51.']
    >>> from natsort import realsorted
    >>> realsorted(a)
    ['a50', 'a+50.300', 'a5.034e1', 'a+50.4', 'a51.']

.. _custom_sort:

Using a Custom Sorting Key
--------------------------

Like the built-in ``sorted`` function, ``natsorted`` can accept a custom
sort key so that:

.. code-block:: python

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
:func:`~natsort_keygen` is a convenient way to generate these keys for you:

.. code-block:: python

    >>> from natsort import natsort_keygen
    >>> a = ['a50', 'a51.', 'a50.4', 'a5.034e1', 'a50.300']
    >>> natsort_key = natsort_keygen(alg=ns.FLOAT)
    >>> a.sort(key=natsort_key)
    >>> a
    ['a50', 'a50.300', 'a5.034e1', 'a50.4', 'a51.']

:func:`~natsort_keygen` has the same API as :func:`~natsorted` (minus the
`reverse` option).

Sorting Multiple Lists According to a Single List
-------------------------------------------------

Sometimes you have multiple lists, and you want to sort one of those
lists and reorder the other lists according to how the first was sorted.
To achieve this you could use the :func:`~index_natsorted` in combination
with the convenience function
:func:`~order_by_index`:

.. code-block:: python

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
``reverse`` option to return the results in reverse order:

.. code-block:: python

    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a, reverse=True)
    ['a10', 'a9', 'a4', 'a2', 'a1']

Sorting Bytes on Python 3
-------------------------

Python 3 is rather strict about comparing strings and bytes, and this
can make it difficult to deal with collections of both. Because of the
challenge of guessing which encoding should be used to decode a bytes
array to a string, :mod:`natsort` does *not* try to guess and automatically
convert for you; in fact, the official stance of :mod:`natsort` is to
not support sorting bytes. Instead, some decoding convenience functions
have been provided to you (see :ref:`bytes_help`) that allow you to
provide a codec for decoding bytes through the ``key`` argument that
will allow :mod:`natsort` to convert byte arrays to strings for sorting;
these functions know not to raise an error if the input is not a byte
array, so you can use the key on any arbitrary collection of data.

.. code-block:: python

    >>> from natsort import as_ascii
    >>> a = [b'a', 14.0, 'b']
    >>> # On Python 2, natsorted(a) would would work as expected.
    >>> # On Python 3, natsorted(a) would raise a TypeError (bytes() < str())
    >>> natsorted(a, key=as_ascii) == [14.0, b'a', 'b']
    True

Additionally, regular expressions cannot be run on byte arrays, making it
so that :mod:`natsort` cannot parse them for numbers. As a result, if you
run :mod:`natsort` on a list of bytes, you will get results that are like
Python's default sorting behavior. Of course, you can use the decoding
functions to solve this:

.. code-block:: python

    >>> from natsort import as_utf8
    >>> a = [b'a56', b'a5', b'a6', b'a40']
    >>> natsorted(a)  # doctest: +SKIP
    [b'a40', b'a5', b'a56', b'a6']
    >>> natsorted(a, key=as_utf8) == [b'a5', b'a6', b'a40', b'a56']
    True

If you need a codec different from ASCII or UTF-8, you can use
:func:`decoder` to generate a custom key:

.. code-block:: python

    >>> from natsort import decoder
    >>> a = [b'a56', b'a5', b'a6', b'a40']
    >>> natsorted(a, key=decoder('latin1')) == [b'a5', b'a6', b'a40', b'a56']
    True

Sorting a Pandas DataFrame
--------------------------

As of Pandas version 0.16.0, the sorting methods do not accept a ``key`` argument,
so you cannot simply pass :func:`natsort_keygen` to a Pandas DataFrame and sort.
This request has been made to the Pandas devs; see
`issue 3942 <https://github.com/pydata/pandas/issues/3942>`_ if you are interested.
If you need to sort a Pandas DataFrame, please check out
`this answer on StackOverflow <http://stackoverflow.com/a/29582718/1399279>`_
for ways to do this without the ``key`` argument to ``sort``.
