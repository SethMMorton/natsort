natsort
=======

.. image:: https://img.shields.io/pypi/v/natsort.svg
    :target: https://pypi.org/project/natsort/

.. image:: https://img.shields.io/pypi/pyversions/natsort.svg
    :target: https://pypi.org/project/natsort/

.. image:: https://img.shields.io/pypi/l/natsort.svg
    :target: https://github.com/SethMMorton/natsort/blob/master/LICENSE

.. image:: https://img.shields.io/travis/SethMMorton/natsort/master.svg?label=travis-ci
    :target: https://travis-ci.org/SethMMorton/natsort

.. image:: https://codecov.io/gh/SethMMorton/natsort/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/SethMMorton/natsort

.. image:: https://api.codacy.com/project/badge/Grade/f2bf04b1fc5d4792bf546f6e497cf4b8
    :target: https://www.codacy.com/app/SethMMorton/natsort

Simple yet flexible natural sorting in Python.

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.org/project/natsort/
    - Documentation: http://natsort.readthedocs.io/

      - `Examples and Recipes <http://natsort.readthedocs.io/en/master/examples.html>`_
      - `How Does Natsort Work? <http://natsort.readthedocs.io/en/master/howitworks.html>`_
      - `API <http://natsort.readthedocs.io/en/master/api.html>`_
      - **NOTE**: The old documentation at pythonhosted.org has been taken down
        with no redirects. Please see
        `this post <https://opensource.stackexchange.com/q/5941/8999>`_ for an
        explanation into why.

    - `FAQ`_
    - `Optional Dependencies`_

      - `fastnumbers <https://pypi.org/project/fastnumbers>`_ >= 2.0.0
      - `PyICU <https://pypi.org/project/PyICU>`_ >= 1.0.0

Quick Description
-----------------

When you try to sort a list of strings that contain numbers, the normal python
sort algorithm sorts lexicographically, so you might not get the results that you
expect:

.. code-block:: python

    >>> a = ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    >>> sorted(a)
    ['1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '2 ft 7 in', '7 ft 6 in']

Notice that it has the order ('1', '10', '2') - this is because the list is
being sorted in lexicographical order, which sorts numbers like you would
letters (i.e. 'b', 'ba', 'c').

``natsort`` provides a function ``natsorted`` that helps sort lists
"naturally" ("naturally" is rather ill-defined, but in general it means
sorting based on meaning and not computer code point).
Using ``natsorted`` is simple:

.. code-block:: python

    >>> from natsort import natsorted
    >>> a = ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    >>> natsorted(a)
    ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 ft 6 in', '10 ft 2 in']

``natsorted`` identifies numbers anywhere in a string and sorts them
naturally. Below are some other things you can do with ``natsort``
(also see the `examples <http://natsort.readthedocs.io/en/master/examples.html>`_
for a quick start guide, or the
`api <http://natsort.readthedocs.io/en/master/api.html>`_ for complete details).

**Note**: ``natsorted`` is designed to be a drop-in replacement for the built-in
``sorted`` function. Like ``sorted``, ``natsorted`` `does not sort in-place`.
To sort a list and assign the output to the same variable, you must
explicitly assign the output to a variable:

.. code-block:: python

    >>> a = ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    >>> natsorted(a)
    ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 ft 6 in', '10 ft 2 in']
    >>> print(a)  # 'a' was not sorted; "natsorted" simply returned a sorted list
    ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    >>> a = natsorted(a)  # Now 'a' will be sorted because the sorted list was assigned to 'a'
    >>> print(a)
    ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 ft 6 in', '10 ft 2 in']

Please see `Generating a Reusable Sorting Key and Sorting In-Place`_ for
an alternate way to sort in-place naturally.

Examples
--------

Sorting Versions
++++++++++++++++

This is handled properly by default (as of ``natsort`` version >= 4.0.0):

.. code-block:: python

    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> natsorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']

If you need to sort release candidates, please see
`this useful hack <http://natsort.readthedocs.io/en/master/examples.html#rc-sorting>`_.

Sorting by Real Numbers (i.e. Signed Floats)
++++++++++++++++++++++++++++++++++++++++++++

This is useful in scientific data analysis and was
the default behavior of ``natsorted`` for ``natsort``
version < 4.0.0. Use the ``realsorted`` function:

.. code-block:: python

    >>> from natsort import realsorted, ns
    >>> # Note that when interpreting as signed floats, the below numbers are
    >>> #            +5.10,                -3.00,            +5.30,              +2.00
    >>> a = ['position5.10.data', 'position-3.data', 'position5.3.data', 'position2.data']
    >>> natsorted(a)
    ['position2.data', 'position5.3.data', 'position5.10.data', 'position-3.data']
    >>> natsorted(a, alg=ns.REAL)
    ['position-3.data', 'position2.data', 'position5.10.data', 'position5.3.data']
    >>> realsorted(a)  # shortcut for natsorted with alg=ns.REAL
    ['position-3.data', 'position2.data', 'position5.10.data', 'position5.3.data']

Locale-Aware Sorting (or "Human Sorting")
+++++++++++++++++++++++++++++++++++++++++

This is where the non-numeric characters are also ordered based on their meaning,
not on their ordinal value, and a locale-dependent thousands separator and decimal
separator is accounted for in the number.
This can be achieved with the ``humansorted`` function:

.. code-block:: python

    >>> a = ['Apple', 'apple15', 'Banana', 'apple14,689', 'banana']
    >>> natsorted(a)
    ['Apple', 'Banana', 'apple14,689', 'apple15', 'banana']
    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    'en_US.UTF-8'
    >>> natsorted(a, alg=ns.LOCALE)
    ['apple15', 'apple14,689', 'Apple', 'banana', 'Banana']
    >>> from natsort import humansorted
    >>> humansorted(a)  # shortcut for natsorted with alg=ns.LOCALE
    ['apple15', 'apple14,689', 'Apple', 'banana', 'Banana']

You may find you need to explicitly set the locale to get this to work
(as shown in the example).
Please see `locale issues <http://natsort.readthedocs.io/en/master/locale_issues.html>`_ and the
`Optional Dependencies`_ section below before using the ``humansorted`` function.

Further Customizing Natsort
+++++++++++++++++++++++++++

If you need to combine multiple algorithm modifiers (such as ``ns.REAL``,
``ns.LOCALE``, and ``ns.IGNORECASE``), you can combine the options using the
bitwise OR operator (``|``). For example,

.. code-block:: python

    >>> a = ['Apple', 'apple15', 'Banana', 'apple14,689', 'banana']
    >>> natsorted(a, alg=ns.REAL | ns.LOCALE | ns.IGNORECASE)
    ['Apple', 'apple15', 'apple14,689', 'Banana', 'banana']
    >>> # The ns enum provides long and short forms for each option.
    >>> ns.LOCALE == ns.L
    True
    >>> # You can also customize the convenience functions, too.
    >>> natsorted(a, alg=ns.REAL | ns.LOCALE | ns.IGNORECASE) == realsorted(a, alg=ns.L | ns.IC)
    True
    >>> natsorted(a, alg=ns.REAL | ns.LOCALE | ns.IGNORECASE) == humansorted(a, alg=ns.R | ns.IC)
    True

All of the available customizations can be found in the documentation for
`the ns enum <http://natsort.readthedocs.io/en/master/ns_class.html>`_.

You can also add your own custom transformation functions with the ``key`` argument.
These can be used with ``alg`` if you wish.

.. code-block:: python

    >>> a = ['apple2.50', '2.3apple']
    >>> natsorted(a, key=lambda x: x.replace('apple', ''), alg=ns.REAL)
    ['2.3apple', 'apple2.50']

Sorting Mixed Types
+++++++++++++++++++

You can mix and match ``int``, ``float``, and ``str`` (or ``unicode``) types
when you sort:

.. code-block:: python

    >>> a = ['4.5', 6, 2.0, '5', 'a']
    >>> natsorted(a)
    [2.0, '4.5', '5', 6, 'a']
    >>> # On Python 2, sorted(a) would return [2.0, 6, '4.5', '5', 'a']
    >>> # On Python 3, sorted(a) would raise an "unorderable types" TypeError

Handling Bytes on Python 3
++++++++++++++++++++++++++

``natsort`` does not officially support the `bytes` type on Python 3, but
convenience functions are provided that help you decode to `str` first:

.. code-block:: python

    >>> from natsort import as_utf8
    >>> a = [b'a', 14.0, 'b']
    >>> # On Python 2, natsorted(a) would would work as expected.
    >>> # On Python 3, natsorted(a) would raise a TypeError (bytes() < str())
    >>> natsorted(a, key=as_utf8) == [14.0, b'a', 'b']
    True
    >>> a = [b'a56', b'a5', b'a6', b'a40']
    >>> # On Python 2, natsorted(a) would would work as expected.
    >>> # On Python 3, natsorted(a) would return the same results as sorted(a)
    >>> natsorted(a, key=as_utf8) == [b'a5', b'a6', b'a40', b'a56']
    True

Generating a Reusable Sorting Key and Sorting In-Place
++++++++++++++++++++++++++++++++++++++++++++++++++++++

Under the hood, ``natsorted`` works by generating a custom sorting
key using ``natsort_keygen`` and then passes that to the built-in
``sorted``. You can use the ``natsort_keygen`` function yourself to
generate a custom sorting key to sort in-place using the ``list.sort``
method.

.. code-block:: python

    >>> from natsort import natsort_keygen
    >>> natsort_key = natsort_keygen()
    >>> a = ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    >>> natsorted(a) == sorted(a, key=natsort_key)
    True
    >>> a.sort(key=natsort_key)
    >>> a
    ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 ft 6 in', '10 ft 2 in']

All of the algorithm customizations mentioned in the `Further Customizing Natsort`_
section can also be applied to ``natsort_keygen`` through the *alg* keyword option.

Other Useful Things
+++++++++++++++++++

 - recursively descend into lists of lists
 - automatic unicode normalization of input data
 - `controlling the case-sensitivity <http://natsort.readthedocs.io/en/master/examples.html#case-sort>`_
 - `sorting file paths correctly <http://natsort.readthedocs.io/en/master/examples.html#path-sort>`_
 - `allow custom sorting keys <http://natsort.readthedocs.io/en/master/examples.html#custom-sort>`_

FAQ
---

How do I debug ``natsort.natsorted()``?
    The best way to debug ``natsorted()`` is to generate a key using ``natsort_keygen()``
    with the same options being passed to ``natsorted``. One can take a look at
    exactly what is being done with their input using this key - it is highly recommended
    to `look at this issue describing how to debug <https://github.com/SethMMorton/natsort/issues/13#issuecomment-50422375>`_
    for *how* to debug, and also to review the
    `How Does Natsort Work? <http://natsort.readthedocs.io/en/master/howitworks.html>`_
    page for *why* ``natsort`` is doing that to your data.

    If you are trying to sort custom classes and running into trouble, please take a look at
    https://github.com/SethMMorton/natsort/issues/60. In short,
    custom classes are not likely to be sorted correctly if one relies
    on the behavior of ``__lt__`` and the other rich comparison operators in their
    custom class - it is better to use a ``key`` function with ``natsort``, or
    use the ``natsort`` key as part of your rich comparison operator definition.

How *does* ``natsort`` work?
    If you don't want to read `How Does Natsort Work? <http://natsort.readthedocs.io/en/master/howitworks.html>`_,
    here is a quick primer.

    ``natsort`` provides a `key function <https://docs.python.org/3/howto/sorting.html#key-functions>`_
    that can be passed to `list.sort() <https://docs.python.org/3/library/stdtypes.html#list.sort>`_
    or `sorted() <https://docs.python.org/3/library/functions.html#sorted>`_ in order to
    modify the default sorting behavior. This key is generated on-demand with the
    key generator ``natsort.natsort_keygen()``.  ``natsort.natsorted()`` is essentially
    a wrapper for the following code:

    .. code-block:: python

        >>> from natsort import natsort_keygen
        >>> natsort_key = natsort_keygen()
        >>> sorted(['1', '10', '2'], key=natsort_key)
        ['1', '2', '10']

    Users can further customize ``natsort`` sorting behavior with the ``key``
    and/or ``alg`` options (see details in the `Further Customizing Natsort`_
    section).

    The key generated by ``natsort_keygen`` *always* returns a ``tuple``. It
    does so in the following way (*some details omitted for clarity*):

      1. Assume the input is a string, and attempt to split it into numbers and
         non-numbers using regular expressions. Numbers are then converted into
         either ``int`` or ``float``.
      2. If the above fails because the input is not a string, assume the input
         is some other sequence (e.g. ``list`` or ``tuple``), and recursively
         apply the key to each element of the sequence.
      3. If the above fails because the input is not iterable, assume the input
         is an ``int`` or ``float``, and just return the input in a ``tuple``.

    Because a ``tuple`` is always returned, a ``TypeError`` should not be common
    unless one tries to do something odd like sort an ``int`` against a ``list``.

``natsort`` gave me results I didn't expect, and it's a terrible library!
    Did you try to debug using the above advice? If so, and you still cannot figure out
    the error, then please `file an issue <https://github.com/SethMMorton/natsort/issues/new>`_.

Shell script
------------

``natsort`` comes with a shell script called ``natsort``, or can also be called
from the command line with ``python -m natsort``. 

Requirements
------------

``natsort`` requires Python version 2.6 or greater or Python 3.3 or greater.
It may run on (but is not tested against) Python 3.2.

Optional Dependencies
---------------------

fastnumbers
+++++++++++

The most efficient sorting can occur if you install the
`fastnumbers <https://pypi.org/project/fastnumbers>`_ package
(version >=0.7.1); it helps with the string to number conversions.
``natsort`` will still run (efficiently) without the package, but if you need
to squeeze out that extra juice it is recommended you include this as a dependency.
``natsort`` will not require (or check) that
`fastnumbers <https://pypi.org/project/fastnumbers>`_ is installed
at installation.

PyICU
+++++

It is recommended that you install `PyICU <https://pypi.org/project/PyICU>`_
if you wish to sort in a locale-dependent manner, see
http://natsort.readthedocs.io/en/master/locale_issues.html for an explanation why.

Installation
------------

Use ``pip``!

.. code-block:: sh

    $ pip install natsort

If you want to install the `Optional Dependencies`_, you can use the
`"extras" notation <https://packaging.python.org/tutorials/installing-packages/#installing-setuptools-extras>`_
at installation time to install those dependencies as well - use ``fast`` for
`fastnumbers <https://pypi.org/project/fastnumbers>`_ and ``icu`` for
`PyICU <https://pypi.org/project/PyICU>`_.

.. code-block:: sh

    # Install both optional dependencies.
    $ pip install natsort[fast,icu]
    # Install just fastnumbers
    $ pip install natsort[fast]

How to Run Tests
----------------

Please note that ``natsort`` is NOT set-up to support ``python setup.py test``.

The recommended way to run tests is with `tox <https://tox.readthedocs.io/en/latest/>`_.
After installing ``tox``, running tests is as simple as executing the following in the
``natsort`` directory:

.. code-block:: sh

    $ tox

``tox`` will create virtual a virtual environment for your tests and install all the
needed testing requirements for you.  You can specify a particular python version
with the ``-e`` flag, e.g. ``tox -e py36``.

If you do not wish to use ``tox``, you can install the testing dependencies and run the
tests manually using `pytest <https://docs.pytest.org/en/latest/>`_ - ``natsort``
contains a ``Pipfile`` for use with `pipenv <https://github.com/pypa/pipenv>`_ that
makes it easy for you to install the testing dependencies:

.. code-block:: sh

    $ pipenv install --skip-lock --dev
    $ pipenv run python -m pytest

Note that above I invoked ``python -m pytest`` instead of just ``pytest`` - this is because
`the former puts the CWD on sys.path <https://docs.pytest.org/en/latest/usage.html#calling-pytest-through-python-m-pytest>`_.

Author
------

Seth M. Morton

History
-------

Please visit the `changelog <http://natsort.readthedocs.io/en/master/changelog.html>`_.
