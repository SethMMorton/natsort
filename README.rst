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
      - `PyICU <https://pypi.python.org/pypi/PyICU>`_

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

``natsort`` provides a function ``natsorted`` that helps sort lists "naturally",
either as real numbers (i.e. signed/unsigned floats or ints), or as versions.
Using ``natsorted`` is simple:

.. code-block:: python

    >>> from natsort import natsorted
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a)
    ['a1', 'a2', 'a4', 'a9', 'a10']

``natsorted`` identifies real numbers anywhere in a string and sorts them
naturally.

Sorting versions is handled properly by default (as of ``natsort`` version >= 4.0.0):

.. code-block:: python

    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> natsorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']

If you need to sort release candidates, please see
`this useful hack <http://pythonhosted.org//natsort/examples.html#rc-sorting>`_ .

You can also perform locale-aware sorting (or "human sorting"), where the
non-numeric characters are ordered based on their meaning (not on their
ordinal value), and local-dependent decimal point and thousands separators
are properly handled; this can be achieved with the ``humansorted`` function:

.. code-block:: python

    >>> a = ['Apple', 'Banana', 'apple', 'banana']
    >>> natsorted(a)
    ['Apple', 'Banana', 'apple', 'banana']
    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    'en_US.UTF-8'
    >>> from natsort import humansorted
    >>> humansorted(a)
    ['apple', 'Apple', 'banana', 'Banana']

You may find you need to explicitly set the locale to get this to work
(as shown in the example).
Please see the `following caveat <http://pythonhosted.org//natsort/examples.html#bug-note>`_
and the `Optional Dependencies`_ section
below before using the ``humansorted`` function, *especially* if you are on a
BSD-based system (like Mac OS X).

You can sort signed floats (i.e. real numbers) using the ``realsorted``; this is
useful in scientific data analysis. This was the default behavior of ``natsorted``
for ``natsort`` version < 4.0.0:

.. code-block:: python

    >>> from natsort import realsorted
    >>> a = ['num5.10', 'num-3', 'num5.3', 'num2']
    >>> natsorted(a)
    ['num2', 'num5.3', 'num5.10', 'num-3']
    >>> realsorted(a)
    ['num-3', 'num2', 'num5.10', 'num5.3']

You can mix and match ``int``, ``float``, and ``str`` (or ``unicode``) types
when you sort:

.. code-block:: python

    >>> a = ['4.5', 6, 2.0, '5', 'a']
    >>> natsorted(a)
    [2.0, '4.5', '5', 6, 'a']
    >>> # On Python 2, sorted(a) would return [2.0, 6, '4.5', '5', 'a']
    >>> # On Python 3, sorted(a) would raise an "unorderable types" TypeError

``natsort`` does not officially support the ``bytes`` type on Python 3, but
convenience functions are provided that help you decode to ``str`` first:

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

The natsort algorithm does other fancy things like 

 - recursively descend into lists of lists
 - control the case-sensitivity
 - sort file paths correctly
 - allow custom sorting keys
 - exposes a natsort_key generator to pass to ``list.sort``

Please see the package documentation for more details, including 
`examples and recipes <http://pythonhosted.org//natsort/examples.html>`_.

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
'''''''''''

The most efficient sorting can occur if you install the 
`fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ package
(version >=0.7.1); it helps with the string to number conversions.
``natsort`` will still run (efficiently) without the package, but if you need
to squeeze out that extra juice it is recommended you include this as a dependency.
``natsort`` will not require (or check) that
`fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ is installed
at installation.

PyICU
'''''

On BSD-based systems (this includes Mac OS X), the underlying ``locale`` library
can be buggy (please see http://bugs.python.org/issue23195); ``locale`` is
used for the ``ns.LOCALE`` option and ``humansorted`` function.. To remedy this,
one can 

    1. Use "\*.ISO8859-1" locale (i.e. 'en_US.ISO8859-1') rather than "\*.UTF-8"
       locale. These locales do not suffer from as many problems as "UTF-8"
       and thus should give expected results.
    2. Use `PyICU <https://pypi.python.org/pypi/PyICU>`_.  If
       `PyICU <https://pypi.python.org/pypi/PyICU>`_ is installed, ``natsort``
       will use it under the hood; this will give more
       reliable cross-platform results in the long run. ``natsort`` will not
       require (or check) that `PyICU <https://pypi.python.org/pypi/PyICU>`_
       is installed at installation. Please visit
       https://github.com/SethMMorton/natsort/issues/21 for more details and
       how to install on Mac OS X. **Please note** that using
       `PyICU <https://pypi.python.org/pypi/PyICU>`_ is the only way to
       guarantee correct results for all input on BSD-based systems, since
       every other suggestion is a workaround.
    3. Do nothing. As of ``natsort`` version 4.0.0, ``natsort`` is configured
       to compensate for a broken ``locale`` library in terms of case-handling;
       if you do not need to be able to properly handle non-ASCII characters
       then this may be the best option for you. 

Note that the above solutions *should not* be required for Windows or
Linux since in Linux-based systems and Windows systems ``locale`` *should* work
just fine.

Author
------

Seth M. Morton

History
-------

These are the last three entries of the changelog.  See the package documentation
for the complete `changelog <http://pythonhosted.org//natsort/changelog.html>`_.

11-01-2015 v. 4.0.4
'''''''''''''''''''

    - Improved coverage of unit tests.
    - Unit tests use new and improved hypothesis library.
    - Fixed compatibility issues with Python 3.5

06-25-2015 v. 4.0.3
'''''''''''''''''''

    - Fixed bad install on last release (sorry guys!).

06-24-2015 v. 4.0.2
'''''''''''''''''''

    - Added back Python 2.6 and Python 3.2 compatibility. Unit testing is now
      performed for these versions.
    - Consolidated under-the-hood compatibility functionality.
