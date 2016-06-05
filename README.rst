natsort
=======

.. image:: https://travis-ci.org/SethMMorton/natsort.svg?branch=master
    :target: https://travis-ci.org/SethMMorton/natsort

.. image:: https://coveralls.io/repos/SethMMorton/natsort/badge.png?branch=master
    :target: https://coveralls.io/r/SethMMorton/natsort?branch=master

Natural sorting for python. 

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.python.org/pypi/natsort
    - Documentation: http://pythonhosted.org/natsort
    - `Optional Dependencies`_

      - `fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ >= 0.7.1
      - `PyICU <https://pypi.python.org/pypi/PyICU>`_ >= 1.0.0

Quick Description
-----------------

When you try to sort a list of strings that contain numbers, the normal python
sort algorithm sorts lexicographically, so you might not get the results that you
expect:

.. code-block:: python

    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a4', 'a9']

Notice that it has the order ('1', '10', '2') - this is because the list is
being sorted in lexicographical order, which sorts numbers like you would
letters (i.e. 'b', 'ba', 'c').

``natsort`` provides a function ``natsorted`` that helps sort lists
"naturally", either as real numbers (i.e. signed/unsigned floats or ints),
or as versions.  Using ``natsorted`` is simple:

.. code-block:: python

    >>> from natsort import natsorted
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a)
    ['a1', 'a2', 'a4', 'a9', 'a10']

``natsorted`` identifies numbers anywhere in a string and sorts them
naturally. Here are some other things you can do with ``natsort``
(please see the `examples <http://pythonhosted.org//natsort/examples.html>`_
for a quick start guide, or the
`api <http://pythonhosted.org//natsort/api.html>`_ for more details).

Sorting Versions
++++++++++++++++

This is handled properly by default (as of ``natsort`` version >= 4.0.0):

.. code-block:: python

    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> natsorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']

If you need to sort release candidates, please see
http://pythonhosted.org//natsort/examples.html#rc-sorting for a useful hack.

Sorting by Real Numbers (i.e. Signed Floats)
++++++++++++++++++++++++++++++++++++++++++++

This is useful in scientific data analysis and was
the default behavior of ``natsorted`` for ``natsort``
version < 4.0.0. Use the ``realsorted`` function:

.. code-block:: python

    >>> from natsort import realsorted, ns
    >>> a = ['num5.10', 'num-3', 'num5.3', 'num2']
    >>> natsorted(a)
    ['num2', 'num5.3', 'num5.10', 'num-3']
    >>> natsorted(a, alg=ns.REAL)
    ['num-3', 'num2', 'num5.10', 'num5.3']
    >>> realsorted(a)  # shortcut for natsorted with alg=ns.REAL
    ['num-3', 'num2', 'num5.10', 'num5.3']

Locale-Aware Sorting (or "Human Sorting")
+++++++++++++++++++++++++++++++++++++++++

This is where the non-numeric characters are ordered based on their meaning,
not on their ordinal value, and a locale-dependent thousands separator
is accounted for in the number.
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
Please see http://pythonhosted.org/natsort/locale_issues.html and the Installation section 
below before using the ``humansorted`` function.

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

Generating a Reusable Sorting Key
+++++++++++++++++++++++++++++++++

All of the ``*sorted`` functions from the ``natsort`` are convenience functions
around the something similar to the following:

.. code-block:: python

    >>> from natsort import natsort_keygen
    >>> natsort_key = natsort_keygen()
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a) == sorted(a, key=natsort_key)
    True

You can use this key for your own use (such as passing to ``list.sort``).
You can also customize the key with the ``ns`` enum
(see `the ns enum <http://pythonhosted.org//natsort/ns_class.html>`_).

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

11-01-2015 v. 4.0.4
+++++++++++++++++++

    - Improved coverage of unit tests.
    - Unit tests use new and improved hypothesis library.
    - Fixed compatibility issues with Python 3.5
