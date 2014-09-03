natsort
=======

.. image:: https://travis-ci.org/SethMMorton/natsort.svg?branch=develop
    :target: https://travis-ci.org/SethMMorton/natsort

.. image:: https://coveralls.io/repos/SethMMorton/natsort/badge.png?branch=develop
    :target: https://coveralls.io/r/SethMMorton/natsort?branch=develop

Natural sorting for python. 

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.python.org/pypi/natsort
    - Documentation: http://pythonhosted.org//natsort/

Quick Description
-----------------

When you try to sort a list of strings that contain numbers, the normal python
sort algorithm sorts lexicographically, so you might not get the results that you
expect::

    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a4', 'a9']

Notice that it has the order ('1', '10', '2') - this is because the list is
being sorted in lexicographical order, which sorts numbers like you would
letters (i.e. 'b', 'ba', 'c').

``natsort`` provides a function ``natsorted`` that helps sort lists "naturally",
either as real numbers (i.e. signed/unsigned floats or ints), or as versions.
Using ``natsorted`` is simple::

    >>> from natsort import natsorted
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a)
    ['a1', 'a2', 'a4', 'a9', 'a10']

``natsorted`` identifies real numbers anywhere in a string and sorts them
naturally.

Sorting version numbers is just as easy with the ``versorted`` function::

    >>> from natsort import versorted
    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> versorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']
    >>> natsorted(a)  # natsorted tries to sort as signed floats, so it won't work
    ['version-2.0', 'version-1.9', 'version-1.11', 'version-1.10']

You can also perform locale-aware sorting (or "human sorting"), where the
non-numeric characters are ordered based on their meaning, not on their
ordinal value; this can be achieved with the ``humansorted`` function::

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
and the "Optional Dependencies" section
below before using the ``humansorted`` function.

You can mix and match ``int``, ``float``, and ``str`` (or ``unicode``) types
when you sort::

    >>> a = ['4.5', 6, 2.0, '5', 'a']
    >>> natsorted(a)
    [2.0, '4.5', '5', 6, 'a']
    >>> # On Python 2, sorted(a) would return [2.0, 6, '4.5', '5', 'a']
    >>> # On Python 3, sorted(a) would raise an "unorderable types" TypeError

The natsort algorithm does other fancy things like 

 - recursively descend into lists of lists
 - control the case-sensitivity
 - sort file paths correctly
 - allow custom sorting keys
 - exposes a natsort_key generator to pass to list.sort

Please see the package documentation for more details, including 
`examples and recipes <http://pythonhosted.org//natsort/examples.html>`_.

Shell script
------------

``natsort`` comes with a shell script called ``natsort``, or can also be called
from the command line with ``python -m natsort``.  The command line script is
only installed onto your ``PATH`` if you don't install via a wheel.  There is
apparently a known bug with the wheel installation process that will not create
entry points.

Requirements
------------

``natsort`` requires python version 2.6 or greater
(this includes python 3.x). To run version 2.6, 3.0, or 3.1 the 
`argparse <https://pypi.python.org/pypi/argparse>`_ module is required.

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

On some systems, Python's ``locale`` library can be buggy (I have found this to be
the case on Mac OS X), so ``natsort`` will use
`PyICU <https://pypi.python.org/pypi/PyICU>`_ under the hood if it is installed
on your computer; this will give more reliable results. ``natsort`` will not
require (or check) that `PyICU <https://pypi.python.org/pypi/PyICU>`_ is installed
at installation.

Depreciation Notices
--------------------

 - In ``natsort`` version 4.0.0, the ``number_type``, ``signed``, ``exp``,
   ``as_path``, and ``py3_safe`` options will be removed from the (documented)
   API, in favor of the ``alg`` option and ``ns`` enum.  They will remain as
   keyword-only arguments after that (for the foreseeable future).
 - In ``natsort`` version 4.0.0, the ``natsort_key`` function will be removed
   from the public API.  All future development should use ``natsort_keygen``
   in preparation for this.
 - In ``natsort`` version 3.1.0, the shell script changed how it interpreted
   input; previously, all input was assumed to be a filepath, but as of 3.1.0
   input is just treated as a string.  For most cases the results are the same.
 
   - As of ``natsort`` version 3.4.0, a ``--path`` option has been added to
     force the shell script to interpret the input as filepaths. 

Author
------

Seth M. Morton

History
-------

These are the last three entries of the changelog.  See the package documentation
for the complete `changelog <http://pythonhosted.org//natsort/changelog.html>`_.

09-02-2014 v. 3.5.0
'''''''''''''''''''

    - Added the 'alg' argument to the 'natsort' functions.  This argument
      accepts an enum that is used to indicate the options the user wishes
      to use.  The 'number_type', 'signed', 'exp', 'as_path', and 'py3_safe'
      options are being depreciated and will become (undocumented)
      keyword-only options in natsort version 4.0.0.
    - The user can now modify how 'natsort' handles the case of non-numeric
      characters.
    - The user can now instruct 'natsort' to use locale-aware sorting, which
      allows 'natsort' to perform true "human sorting".

      - The `humansorted` convenience function has been included to make this
        easier.

    - Updated shell script with locale functionality.

08-12-2014 v. 3.4.1
'''''''''''''''''''

    - 'natsort' will now use the 'fastnumbers' module if it is installed. This
      gives up to an extra 30% boost in speed over the previous performance
      enhancements.
    - Made documentation point to more 'natsort' resources, and also added a
      new example in the examples section.

07-19-2014 v. 3.4.0
'''''''''''''''''''

    - Fixed a bug that caused user's options to the 'natsort_key' to not be
      passed on to recursive calls of 'natsort_key'.
    - Added a 'natsort_keygen' function that will generate a wrapped version
      of 'natsort_key' that is easier to call.  'natsort_key' is now set to
      depreciate at natsort version 4.0.0.
    - Added an 'as_path' option to 'natsorted' & co. that will try to treat
      input strings as filepaths. This will help yield correct results for
      OS-generated inputs like
      ``['/p/q/o.x', '/p/q (1)/o.x', '/p/q (10)/o.x', '/p/q/o (1).x']``.
    - Massive performance enhancements for string input (1.8x-2.0x), at the expense
      of reduction in speed for numeric input (~2.0x).

      - This is a good compromise because the most common input will be strings,
        not numbers, and sorting numbers still only takes 0.6x the time of sorting
        strings.  If you are sorting only numbers, you would use 'sorted' anyway.

    - Added the 'order_by_index' function to help in using the output of
      'index_natsorted' and 'index_versorted'.
    - Added the 'reverse' option to 'natsorted' & co. to make it's API more
      similar to the builtin 'sorted'.
    - Added more unit tests.
    - Added auxiliary test code that helps in profiling and stress-testing.
    - Reworked the documentation, moving most of it to PyPI's hosting platform.
    - Added support for coveralls.io.
    - Entire codebase is now PyFlakes and PEP8 compliant.
