natsort
=======

.. image:: https://api.codacy.com/project/badge/Grade/f2bf04b1fc5d4792bf546f6e497cf4b8
   :alt: Codacy Badge
   :target: https://www.codacy.com/app/SethMMorton/natsort?utm_source=github.com&utm_medium=referral&utm_content=SethMMorton/natsort&utm_campaign=badger

.. image:: https://travis-ci.org/SethMMorton/natsort.svg?branch=master
    :target: https://travis-ci.org/SethMMorton/natsort

.. image:: https://coveralls.io/repos/SethMMorton/natsort/badge.png?branch=master
    :target: https://coveralls.io/r/SethMMorton/natsort?branch=master

Natural sorting for python. 

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.python.org/pypi/natsort
    - Documentation: http://pythonhosted.org/natsort

      - `Examples and Recipes <http://pythonhosted.org//natsort/examples.html>`_
      - `How Does Natsort Work? <http://pythonhosted.org//natsort/howitworks.html>`_
      - `API <http://pythonhosted.org//natsort/api.html>`_

    - `Optional Dependencies`_

      - `fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ >= 0.7.1
      - `PyICU <https://pypi.python.org/pypi/PyICU>`_ >= 1.0.0

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
(also see the `examples <http://pythonhosted.org//natsort/examples.html>`_
for a quick start guide, or the
`api <http://pythonhosted.org//natsort/api.html>`_ for complete details).

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

Sorting Versions
++++++++++++++++

This is handled properly by default (as of ``natsort`` version >= 4.0.0):

.. code-block:: python

    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> natsorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']

If you need to sort release candidates, please see
`this useful hack <http://pythonhosted.org//natsort/examples.html#rc-sorting>`_.

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
Please see `locale issues <http://pythonhosted.org/natsort/locale_issues.html>`_ and the
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
`the ns enum <http://pythonhosted.org//natsort/ns_class.html>`_.

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
 - `controlling the case-sensitivity <http://pythonhosted.org//natsort/examples.html#case-sort>`_
 - `sorting file paths correctly <http://pythonhosted.org//natsort/examples.html#path-sort>`_
 - `allow custom sorting keys <http://pythonhosted.org//natsort/examples.html#custom-sort>`_

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
`fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ package
(version >=0.7.1); it helps with the string to number conversions.
``natsort`` will still run (efficiently) without the package, but if you need
to squeeze out that extra juice it is recommended you include this as a dependency.
``natsort`` will not require (or check) that
`fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ is installed
at installation.

PyICU
+++++

It is recommended that you install `PyICU <https://pypi.python.org/pypi/PyICU>`_
if you wish to sort in a locale-dependent manner, see
http://pythonhosted.org/natsort/locale_issues.html for an explanation why.

Author
------

Seth M. Morton

History
-------

These are the last three entries of the changelog.  See the package documentation
for the complete `changelog <http://pythonhosted.org//natsort/changelog.html>`_.

01-02-2017 v. 5.0.2
+++++++++++++++++++

    - Added additional unicode number support for Python 3.6.
    - Renamed several internal functions and variables to improve clarity.
    - Improved documentation examples.
    - Added a "how does it work?" section to the documentation.

06-04-2016 v. 5.0.1
+++++++++++++++++++

    - The ``ns`` enum attributes can now be imported from the top-level
      namespace.
    - Fixed a bug with the ``from natsort import *`` mechanism.
    - Fixed bug with using ``natsort`` with ``python -OO``.

05-08-2016 v. 5.0.0
+++++++++++++++++++

    - ``ns.LOCALE``/``humansorted`` now accounts for thousands separators.
    - Refactored entire codebase to be more functional (as in use functions as
      units). Previously, the code was rather monolithic and difficult to follow. The
      goal is that with the code existing in smaller units, contributing will
      be easier.
    - Deprecated ``ns.TYPESAFE`` option as it is now always on (due to a new
      iterator-based algorithm, the typesafe function is now cheap).
    - Increased speed of execution (came for free with the new functional approach
      because the new factory function paradigm eliminates most ``if`` branches
      during execution).

      - For the most cases, the code is 30-40% faster than version 4.0.4.
      - If using ``ns.LOCALE`` or ``humansorted``, the code is 1100% faster than
        version 4.0.4.

    - Improved clarity of documentaion with regards to locale-aware sorting.
    - Added a new ``chain_functions`` function for convenience in creating
      a complex user-given ``key`` from several existing functions.
