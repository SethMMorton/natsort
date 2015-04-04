natsort
=======

.. image:: https://travis-ci.org/SethMMorton/natsort.svg?branch=master
    :target: https://travis-ci.org/SethMMorton/natsort

.. image:: https://coveralls.io/repos/SethMMorton/natsort/badge.png?branch=master
    :target: https://coveralls.io/r/SethMMorton/natsort?branch=master

Natural sorting for python. 

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.python.org/pypi/natsort
    - Documentation: http://pythonhosted.org/natsort/

Please see `Deprecation Notices`_ for an `important` backwards incompatibility notice
for ``natsort`` version 4.0.0.

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

Sorting version numbers is just as easy with the ``versorted`` function:

.. code-block:: python

    >>> from natsort import versorted
    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> versorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']
    >>> natsorted(a)  # natsorted tries to sort as signed floats, so it won't work
    ['version-2.0', 'version-1.9', 'version-1.11', 'version-1.10']

You can also perform locale-aware sorting (or "human sorting"), where the
non-numeric characters are ordered based on their meaning, not on their
ordinal value; this can be achieved with the ``humansorted`` function:

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

You can mix and match ``int``, ``float``, and ``str`` (or ``unicode``) types
when you sort:

.. code-block:: python

    >>> a = ['4.5', 6, 2.0, '5', 'a']
    >>> natsorted(a)
    [2.0, '4.5', '5', 6, 'a']
    >>> # On Python 2, sorted(a) would return [2.0, 6, '4.5', '5', 'a']
    >>> # On Python 3, sorted(a) would raise an "unorderable types" TypeError

You cannot mix and match ``str`` and ``bytes`` objects on Python 3.

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

``natsort`` requires python version 2.6 or greater
(this includes python 3.x). To run version 2.6, 3.0, or 3.1 the 
`argparse <https://pypi.python.org/pypi/argparse>`_ module is required.

.. _optional:

Optional Dependencies
---------------------

fastnumbers
'''''''''''

The most efficient sorting can occur if you install the 
`fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ package (it helps
with the string to number conversions.)  ``natsort`` will still run (efficiently)
without the package, but if you need to squeeze out that extra juice it is
recommended you include this as a dependency.  ``natsort`` will not require (or
check) that `fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ is installed
at installation.

PyICU
'''''

On BSD-based systems (this includes Mac OS X), the underlying ``locale`` library
can be buggy (please see http://bugs.python.org/issue23195), so ``natsort`` will use
`PyICU <https://pypi.python.org/pypi/PyICU>`_ under the hood if it is installed
on your computer; this will give more reliable cross-platform results.
``natsort`` will not require (or check) that
`PyICU <https://pypi.python.org/pypi/PyICU>`_ is installed at installation
since in Linux-based systems and Windows systems ``locale`` should work just fine.
Please visit https://github.com/SethMMorton/natsort/issues/21 for more details and
how to install on Mac OS X.

.. _deprecate:

Deprecation Notices
-------------------

 - The default sorting algorithm for ``natsort`` will change in version 4.0.0
   from signed floats (with exponents) to unsigned integers. The motivation
   for this change is that it will cause ``natsort`` to return results that
   pass the "least astonishment" test for the most common use case, which is
   sorting version numbers. If you currently rely on the default behavior
   to be signed floats, it is recommend that you add ``alg=ns.F`` to your
   ``natsort`` calls or switch to the new ``realsorted`` function which
   behaves identically to the current ``natsorted`` with default values.
 - In ``natsort`` version 4.0.0, the ``number_type``, ``signed``, ``exp``,
   ``as_path``, and ``py3_safe`` options will be removed from the (documented)
   API, in favor of the ``alg`` option and ``ns`` enum.  They will remain as
   keyword-only arguments after that (for the foreseeable future).
 - In ``natsort`` version 4.0.0, the ``natsort_key`` function will be removed
   from the public API.  All future development should use ``natsort_keygen``
   in preparation for this.

Author
------

Seth M. Morton

History
-------

These are the last three entries of the changelog.  See the package documentation
for the complete `changelog <http://pythonhosted.org//natsort/changelog.html>`_.

04-04-2015 v. 3.5.4
'''''''''''''''''''

    - Added 'realsorted' and 'index_realsorted' functions for
      forward-compatibility with >= 4.0.0.
    - Made explanation of when to use "TYPESAFE" more clear in the docs.

04-02-2015 v. 3.5.4
'''''''''''''''''''

    - Fixed bug where a 'TypeError' was raised if a string containing a leading
      number was sorted with alpha-only strings when 'LOCALE' is used.

03-26-2015 v. 3.5.3
'''''''''''''''''''

    - Fixed bug where '--reverse-filter; option in shell script was not
      getting checked for correctness.
    - Documentation updates to better describe locale bug, and illustrate
      upcoming default behavior change.
    - Internal improvements, including making test suite more granular.

01-13-2015 v. 3.5.2
'''''''''''''''''''

    - Enhancement that will convert a 'pathlib.Path' object to a 'str' if
      'ns.PATH' is enabled.
