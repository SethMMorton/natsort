.. default-domain:: py
.. currentmodule:: natsort

.. _examples:

Examples and Recipes
====================

If you want more detailed examples than given on this page, please see
https://github.com/SethMMorton/natsort/tree/master/tests.

.. contents::
    :local:

Basic Usage
-----------

In the most basic use case, simply import :func:`~natsorted` and use
it as you would :func:`sorted`:

.. code-block:: pycon

    >>> a = ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    >>> sorted(a)
    ['1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '2 ft 7 in', '7 ft 6 in']
    >>> from natsort import natsorted, ns
    >>> natsorted(a)
    ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 ft 6 in', '10 ft 2 in']

Sort Version Numbers
--------------------

As of :mod:`natsort` version >= 4.0.0, :func:`~natsorted` will work for
well-behaved version numbers, like ``MAJOR.MINOR.PATCH``.

.. _rc_sorting:

Sorting More Expressive Versioning Schemes
++++++++++++++++++++++++++++++++++++++++++

By default, if you wish to sort versions that are not as simple as
``MAJOR.MINOR.PATCH`` (or similar), you may not get the results you expect:

.. code-block:: pycon

    >>> a = ['1.2', '1.2rc1', '1.2beta2', '1.2beta1', '1.2alpha', '1.2.1', '1.1', '1.3']
    >>> natsorted(a)
    ['1.1', '1.2', '1.2.1', '1.2alpha', '1.2beta1', '1.2beta2', '1.2rc1', '1.3']

To make the '1.2' pre-releases come before '1.2.1', you need to use the
following recipe:

.. code-block:: pycon

    >>> natsorted(a, key=lambda x: x.replace('.', '~'))
    ['1.1', '1.2', '1.2alpha', '1.2beta1', '1.2beta2', '1.2rc1', '1.2.1', '1.3']

If you also want '1.2' after all the alpha, beta, and rc candidates, you can
modify the above recipe:

.. code-block:: pycon

    >>> natsorted(a, key=lambda x: x.replace('.', '~')+'z')
    ['1.1', '1.2alpha', '1.2beta1', '1.2beta2', '1.2rc1', '1.2', '1.2.1', '1.3']

Please see `this issue <https://github.com/SethMMorton/natsort/issues/13>`_ to
see why this works.

Sorting Rigorously Defined Versioning Schemes (e.g. SemVer or PEP 440)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

If you know you are using a versioning scheme that follows a well-defined format
for which there is third-party module support, you should use those modules
to assist in sorting. Some examples might be
`PEP 440 <https://packaging.pypa.io/en/latest/version>`_ or
`SemVer <https://python-semver.readthedocs.io/en/latest/api.html>`_.

If we are being honest, using these methods to parse a version means you don't
need to use :mod:`natsort` - you should probably just use :func:`sorted`
directly. Here's an example with SemVer:

.. code-block:: pycon

    >>> from semver import VersionInfo
    >>> a = ['3.4.5-pre.1', '3.4.5', '3.4.5-pre.2+build.4']
    >>> sorted(a, key=VersionInfo.parse)
    ['3.4.5-pre.1', '3.4.5-pre.2+build.4', '3.4.5']

.. _path_sort:

Sort OS-Generated Paths
-----------------------

In some cases when sorting file paths with OS-Generated names, the default
:mod:`~natsorted` algorithm may not be sufficient.  In cases like these,
you may need to use the ``ns.PATH`` option:

.. code-block:: pycon

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

.. code-block:: pycon

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

.. code-block:: pycon

    >>> a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    >>> natsorted(a)
    ['Apple', 'Banana', 'Corn', 'apple', 'banana', 'corn']

There are times when you wish to ignore the case when sorting,
you can easily do this with the ``ns.IGNORECASE`` option:

.. code-block:: pycon

    >>> natsorted(a, alg=ns.IGNORECASE)
    ['Apple', 'apple', 'Banana', 'banana', 'corn', 'Corn']

Note thats since Python's sorting is stable, the order of equivalent
elements after lowering the case is the same order they appear in the
original list.

Upper-case letters appear first in the ASCII table, but many natural
sorting methods place lower-case first.  To do this, use
``ns.LOWERCASEFIRST``:

.. code-block:: pycon

    >>> natsorted(a, alg=ns.LOWERCASEFIRST)
    ['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']

It may be undesirable to have the upper-case letters grouped together
and the lower-case letters grouped together; most would expect all
"a"s to bet together regardless of case, and all "b"s, and so on. To
achieve this, use ``ns.GROUPLETTERS``:

.. code-block:: pycon

    >>> natsorted(a, alg=ns.GROUPLETTERS)
    ['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']

You might combine this with ``ns.LOWERCASEFIRST`` to get what most
would expect to be "natural" sorting:

.. code-block:: pycon

    >>> natsorted(a, alg=ns.G | ns.LF)
    ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']

Customizing Float Definition
----------------------------

You can make :func:`~natsorted` search for any float that would be
a valid Python float literal, such as 5, 0.4, -4.78, +4.2E-34, etc.
using the ``ns.FLOAT`` key. You can disable the exponential component
of the number with ``ns.NOEXP``.

.. code-block:: pycon

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

.. code-block:: pycon

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

.. code-block:: pycon

    >>> from operator import attrgetter, itemgetter
    >>> a = [['a', 'num4'], ['b', 'num8'], ['c', 'num2']]
    >>> natsorted(a, key=itemgetter(1))
    [['c', 'num2'], ['a', 'num4'], ['b', 'num8']]
    >>> class Foo:
    ...    def __init__(self, bar):
    ...        self.bar = bar
    ...    def __repr__(self):
    ...        return "Foo('{}')".format(self.bar)
    >>> b = [Foo('num3'), Foo('num5'), Foo('num2')]
    >>> natsorted(b, key=attrgetter('bar'))
    [Foo('num2'), Foo('num3'), Foo('num5')]

.. _unit_sorting:

Accounting for Units When Sorting
+++++++++++++++++++++++++++++++++

:mod:`natsort` does not come with any pre-built mechanism to sort units,
but you can write your own `key` to do this. Below, I will demonstrate sorting
imperial lengths (e.g. feet an inches), but of course you can extend this to any
set of units you need. This example is based on code
`from this issue <https://github.com/SethMMorton/natsort/issues/100#issuecomment-530659310>`_,
and uses the function :func:`natsort.numeric_regex_chooser` to build a regular
expression that will parse numbers in the same manner as :mod:`natsort` itself.

.. code-block:: pycon

    >>> import re
    >>> import natsort
    >>>
    >>> # Define how each unit will be transformed
    >>> conversion_mapping = {
    ...         "in": 1,
    ...         "inch": 1,
    ...         "inches": 1,
    ...         "ft": 12,
    ...         "feet": 12,
    ...         "foot": 12,
    ... }
    >>>
    >>> # This regular expression searches for numbers and units
    >>> all_units = "|".join(conversion_mapping.keys())
    >>> float_re = natsort.numeric_regex_chooser(natsort.FLOAT | natsort.SIGNED)
    >>> unit_finder = re.compile(r"({})\s*({})".format(float_re, all_units), re.IGNORECASE)
    >>>
    >>> def unit_replacer(matchobj):
    ...     """
    ...     Given a regex match object, return a replacement string where units are modified
    ...     """
    ...     number = matchobj.group(1)
    ...     unit = matchobj.group(2)
    ...     new_number = float(number) * conversion_mapping[unit]
    ...     return "{} in".format(new_number)
    ...
    >>> # Demo time!
    >>> data = ['1 ft', '5 in', '10 ft', '2 in']
    >>> [unit_finder.sub(unit_replacer, x) for x in data]
    ['12.0 in', '5.0 in', '120.0 in', '2.0 in']
    >>>
    >>> natsort.natsorted(data, key=lambda x: unit_finder.sub(unit_replacer, x))
    ['2 in', '5 in', '1 ft', '10 ft']

Generating a Natsort Key
------------------------

If you need to sort a list in-place, you cannot use :func:`~natsorted`; you
need to pass a key to the :meth:`list.sort` method. The function
:func:`~natsort_keygen` is a convenient way to generate these keys for you:

.. code-block:: pycon

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

.. code-block:: pycon

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

.. code-block:: pycon

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

.. code-block:: pycon

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

.. code-block:: pycon

    >>> from natsort import as_utf8
    >>> a = [b'a56', b'a5', b'a6', b'a40']
    >>> natsorted(a)  # doctest: +SKIP
    [b'a40', b'a5', b'a56', b'a6']
    >>> natsorted(a, key=as_utf8) == [b'a5', b'a6', b'a40', b'a56']
    True

If you need a codec different from ASCII or UTF-8, you can use
:func:`decoder` to generate a custom key:

.. code-block:: pycon

    >>> from natsort import decoder
    >>> a = [b'a56', b'a5', b'a6', b'a40']
    >>> natsorted(a, key=decoder('latin1')) == [b'a5', b'a6', b'a40', b'a56']
    True

Sorting a Pandas DataFrame
--------------------------

Starting from Pandas version 1.1.0, the
`sorting methods accept a "key" argument <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html>`_,
so you can simply pass :func:`natsort_keygen` to the sorting methods and sort:

.. code-block:: python

    import pandas as pd
    from natsort import natsort_keygen
    s = pd.Series(['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in'])
    s.sort_values(key=natsort_keygen())
    # 1     1 ft 5 in
    # 0     2 ft 7 in
    # 3    2 ft 11 in
    # 4     7 ft 6 in
    # 2    10 ft 2 in
    # dtype: object

Similarly, if you need to sort the index there is
`sort_index <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_index.html>`_
of a DataFrame.

If you are on an older version of Pandas, check out please check out
`this answer on StackOverflow <https://stackoverflow.com/a/29582718/1399279>`_
for ways to do this without the ``key`` argument to ``sort_values``.
