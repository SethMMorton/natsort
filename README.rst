natsort
=======

.. image:: https://travis-ci.org/SethMMorton/natsort.svg?branch=master
    :target: https://travis-ci.org/SethMMorton/natsort

Natural sorting for python.  ``natsort`` requires python version 2.6 or greater
(this includes python 3.x). To run version 2.6, 3.0, or 3.1 the 
`argparse <https://pypi.python.org/pypi/argparse>`_ module is required.

``natsort`` comes with a shell script that is described below.  You can
also execute ``natsort`` from the command line with ``python -m natsort``.

Problem Statement
-----------------

When you try to sort a list of strings that contain numbers, the normal python
sort algorithm sorts lexicographically, so you might not get the results that you
expect::

    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a4', 'a9']

Notice that it has the order ('1', '10', '2') - this is because the list is
being sorted in lexicographical order, which sorts numbers like you would
letters (i.e. 'a', 'at', 'b').  It would be better if you had a sorting
algorithm that recognized numbers as numbers and treated them like numbers,
not letters.

This is where ``natsort`` comes in: it provides a key that helps sort lists
"naturally".  It provides support for ints and floats (including negatives and
exponential notation), and also a function specifically for sorting version
numbers.

Synopsis
--------

Using ``natsort`` is simple::

    >>> from natsort import natsorted
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a)
    ['a1', 'a2', 'a4', 'a9', 'a10']

``natsort`` identifies the numbers and sorts them separately from strings.

You can also mix and match ``int``, ``float``, and ``str`` (or ``unicode``) types
when you sort::

    >>> a = ['4.5', 6, 2.0, '5', 'a']
    >>> natsorted(a)
    [2.0, '4.5', '5', 6, 'a']
    >>> # On Python 2, sorted(a) would return [2.0, 6, '4.5', '5', 'a']
    >>> # On Python 3, sorted(a) would raise an "unorderable types" TypeError

The natsort algorithm will recursively descend into lists of lists so you can sort by
the sublist contents::

    >>> data = [['a1', 'a5'], ['a1', 'a40'], ['a10', 'a1'], ['a2', 'a5']]
    >>> sorted(data)
    [['a1', 'a40'], ['a1', 'a5'], ['a10', 'a1'], ['a2', 'a5']]
    >>> natsorted(data)
    [['a1', 'a5'], ['a1', 'a40'], ['a2', 'a5'], ['a10', 'a1']]

There is also a special convenience function provided that is best for sorting
version numbers::

    >>> from natsort import versorted
    >>> a = ['ver-2.9.9a', 'ver-1.11', 'ver-2.9.9b', 'ver-1.11.4', 'ver-1.10.1']
    >>> versorted(a)
    ['ver-1.10.1', 'ver-1.11', 'ver-1.11.4', 'ver-2.9.9a', 'ver-2.9.9b']

The Sorting Algorithms
''''''''''''''''''''''

Sometimes you want to sort by floats, sometimes by ints, and sometimes simply
by digits.  ``natsort`` supports all three number types.  They can be chosen
with the ``number_type`` argument to ``natsorted``.

Sort by floats
++++++++++++++

By default, ``natsort`` searches for floats (even in exponential
notation!).  This means that it will look for things like negative
signs and decimal points when determining a number::

    >>> a = ['a50', 'a51.', 'a50.4', 'a5.034e1', 'a50.300']
    >>> sorted(a)
    ['a5.034e1', 'a50', 'a50.300', 'a50.4', 'a51.']
    >>> natsorted(a, number_type=float)
    ['a50', 'a50.300', 'a5.034e1', 'a50.4', 'a51.']
    >>> natsorted(a) # Float is the default behavior
    ['a50', 'a50.300', 'a5.034e1', 'a50.4', 'a51.']

Sort by ints
++++++++++++

In some cases you don't want ``natsort`` to identify your numbers as floats,
particularly if you are sorting version numbers.  This is because you want the
version '1.10' to come after '1.2', not before. In that case, it is advantageous
to sort by ints, not floats::

    >>> a = ['ver1.9.9a', 'ver1.11', 'ver1.9.9b', 'ver1.11.4', 'ver1.10.1']
    >>> sorted(a)
    ['ver1.10.1', 'ver1.11', 'ver1.11.4', 'ver1.9.9a', 'ver1.9.9b']
    >>> natsorted(a)
    ['ver1.10.1', 'ver1.11', 'ver1.11.4', 'ver1.9.9a', 'ver1.9.9b']
    >>> natsorted(a, number_type=int)
    ['ver1.9.9a', 'ver1.9.9b', 'ver1.10.1', 'ver1.11', 'ver1.11.4']

Sort by digits (best for version numbers)
+++++++++++++++++++++++++++++++++++++++++

The only difference between sorting by ints and sorting by digits is that
sorting by ints may take into account a negative sign, and sorting by digits
will not.  This may be an issue if you used a '-' as your separator before the
version numbers.  Essentially this is a shortcut for a number type of ``int``
and the ``signed`` option of ``False``::

    >>> a = ['ver-2.9.9a', 'ver-1.11', 'ver-2.9.9b', 'ver-1.11.4', 'ver-1.10.1']
    >>> natsorted(a, number_type=int)
    ['ver-2.9.9a', 'ver-2.9.9b', 'ver-1.10.1', 'ver-1.11', 'ver-1.11.4']
    >>> natsorted(a, number_type=None)
    ['ver-1.10.1', 'ver-1.11', 'ver-1.11.4', 'ver-2.9.9a', 'ver-2.9.9b']

The ``versorted`` function is simply a wrapper for ``number_type=None``,
and if you need to sort just version numbers it is best to use the
``versorted`` function for clarity::

    >>> natsorted(a, number_type=None) == versorted(a)
    True

Using a sorting key
'''''''''''''''''''

Like the built-in ``sorted`` function, ``natsorted`` can accept a key so that 
you can sort based on a particular item of a list or by an attribute of a class::

    >>> from operator import attrgetter, itemgetter
    >>> a = [['num4', 'b'], ['num8', 'c'], ['num2', 'a']]
    >>> natsorted(a, key=itemgetter(0))
    [['num2', 'a'], ['num4', 'b'], ['num8', 'c']]
    >>> class Foo:
    ...    def __init__(self, bar):
    ...        self.bar = bar
    ...    def __repr__(self):
    ...        return "Foo('{0}')".format(self.bar)
    >>> b = [Foo('num3'), Foo('num5'), Foo('num2')]
    >>> natsorted(b, key=attrgetter('bar'))
    [Foo('num2'), Foo('num3'), Foo('num5')]

API
---

The ``natsort`` package provides five functions: ``natsort_key``,
``natsorted``, ``versorted``, ``index_natsorted``, and ``index_versorted``.
You can look at the unit tests to see more thorough examples of how
``natsort`` can be used.

natsorted
'''''''''

``natsort.natsorted`` (*sequence*, *key* = ``lambda x: x``, *number_type* = ``float``, *signed* = ``True``, *exp* = ``True``)

    sequence (*iterable*)
        The sequence to sort.

    key (*function*)
        A key used to determine how to sort each element of the sequence.

    number_type (``None``, ``float``, ``int``)
        The types of number to sort by: ``float`` searches for floating point numbers,
        ``int`` searches for integers, and ``None`` searches for digits (like integers 
        but does not take into account negative sign). ``None`` is a shortcut for 
        ``number_type = int`` and ``signed = False``. 

    signed (``True``, ``False``)
        By default a '+' or '-' before a number is taken to be the sign of the number.
        If ``signed`` is ``False``, any '+' or '-' will not be considered to be part
        of the number, but as part of the string.

    exp (``True``, ``False``)
        This option only applies to ``number_type = float``.  If ``exp = True``, a string
        like ``"3.5e5"`` will be interpreted as ``350000``, i.e. the exponential part
        is considered to be part of the number.  If ``exp = False``, ``"3.5e5"`` is
        interpreted as ``(3.5, "e", 5)``.  The default behavior is ``exp = True``.

    returns
        The sorted sequence.

Use ``natsorted`` just like the builtin ``sorted``::

    >>> from natsort import natsorted
    >>> a = ['num3', 'num5', 'num2']
    >>> natsorted(a)
    ['num2', 'num3', 'num5']

versorted
'''''''''

``natsort.versorted`` (*sequence*, *key* = ``lambda x: x``)

    sequence (*iterable*)
        The sequence to sort.

    key (*function*)
        A key used to determine how to sort each element of the sequence.

    returns
        The sorted sequence.

Use ``versorted`` just like the builtin ``sorted``::

    >>> from natsort import versorted
    >>> a = ['num4.0.2', 'num3.4.1', 'num3.4.2']
    >>> versorted(a)
    ['num3.4.1', 'num3.4.2', 'num4.0.2']

This is a wrapper around ``natsorted(seq, number_type=None)``, and is used
to easily sort version numbers.

index_natsorted
'''''''''''''''

``natsort.index_natsorted`` (*sequence*, *key* = ``lambda x: x``, *number_type* = ``float``, *signed* = ``True``, *exp* = ``True``)

    sequence (*iterable*)
        The sequence to sort.

    key (*function*)
        A key used to determine how to sort each element of the sequence.

    number_type (``None``, ``float``, ``int``)
        The types of number to sort on: ``float`` searches for floating point numbers,
        ``int`` searches for integers, and ``None`` searches for digits (like integers 
        but does not take into account negative sign). ``None`` is a shortcut for 
        ``number_type = int`` and ``signed = False``. 

    signed (``True``, ``False``)
        By default a '+' or '-' before a number is taken to be the sign of the number.
        If ``signed`` is ``False``, any '+' or '-' will not be considered to be part
        of the number, but as part part of the string.

    exp (``True``, ``False``)
        This option only applies to ``number_type = float``.  If ``exp = True``, a string
        like ``"3.5e5"`` will be interpreted as ``350000``, i.e. the exponential part
        is considered to be part of the number.  If ``exp = False``, ``"3.5e5"`` is
        interpreted as ``(3.5, "e", 5)``.  The default behavior is ``exp = True``.

    returns
        The ordered indexes of the sequence.

Use ``index_natsorted`` if you want to sort multiple lists by the sort order of
one list::

    >>> from natsort import index_natsorted
    >>> a = ['num3', 'num5', 'num2']
    >>> b = ['foo', 'bar', 'baz']
    >>> index = index_natsorted(a)
    >>> index
    [2, 0, 1]
    >>> # Sort both lists by the sort order of a
    >>> [a[i] for i in index]
    ['num2', 'num3', 'num5']
    >>> [b[i] for i in index]
    ['baz', 'foo', 'bar']

index_versorted
'''''''''''''''

``natsort.index_versorted`` (*sequence*, *key* = ``lambda x: x``)

    sequence (*iterable*)
        The sequence to sort.

    key (*function*)
        A key used to determine how to sort each element of the sequence.

    returns
        The ordered indexes of the sequence.

Use ``index_versorted`` just like the builtin sorted::

    >>> from natsort import index_versorted
    >>> a = ['num4.0.2', 'num3.4.1', 'num3.4.2']
    >>> index_versorted(a)
    [1, 2, 0]

This is a wrapper around ``index_natsorted(seq, number_type=None)``, and is used
to easily sort version numbers by their indexes.

natsort_key
'''''''''''

``natsort.natsort_key`` (value, *number_type* = ``float``, *signed* = ``True``, *exp* = ``True``, *py3_safe* = ``False``)

    value
        The value used by the sorting algorithm

    number_type (``None``, ``float``, ``int``)
        The types of number to sort on: ``float`` searches for floating point numbers,
        ``int`` searches for integers, and ``None`` searches for digits (like integers 
        but does not take into account negative sign). ``None`` is a shortcut for 
        ``number_type = int`` and ``signed = False``. 

    signed (``True``, ``False``)
        By default a '+' or '-' before a number is taken to be the sign of the number.
        If ``signed`` is ``False``, any '+' or '-' will not be considered to be part
        of the number, but as part part of the string.

    exp (``True``, ``False``)
        This option only applies to ``number_type = float``.  If ``exp = True``, a string
        like ``"3.5e5"`` will be interpreted as ``350000``, i.e. the exponential part
        is considered to be part of the number.  If ``exp = False``, ``"3.5e5"`` is
        interpreted as ``(3.5, "e", 5)``.  The default behavior is ``exp = True``.

    py3_safe (``True``, ``False``)
        This will make the string parsing algorithm be more careful by placing
        an empty string between two adjacent numbers after the parsing algorithm.
        This will prevent the "unorderable types" error.

    returns
        The modified value with numbers extracted.

Using ``natsort_key`` is just like any other sorting key in python::

    >>> from natsort import natsort_key
    >>> a = ['num3', 'num5', 'num2']
    >>> a.sort(key=natsort_key)
    >>> a
    ['num2', 'num3', 'num5']

It works by separating out the numbers from the strings::

    >>> natsort_key('num2')
    ('num', 2.0)

If you need to call ``natsort_key`` with the ``number_type`` argument, or get a special
attribute or item of each element of the sequence, the easiest way is to make a 
``lambda`` expression that calls ``natsort_key``::

    >>> from operator import itemgetter
    >>> a = [['num4', 'b'], ['num8', 'c'], ['num2', 'a']]
    >>> f = itemgetter(0)
    >>> a.sort(key=lambda x: natsort_key(f(x), number_type=int))
    >>> a
    [['num2', 'a'], ['num4', 'b'], ['num8', 'c']]

Shell Script
------------

For your convenience, there is a ``natsort`` shell script supplied to you that
allows you to call ``natsort`` from the command-line.  ``natsort`` was written to
aid in computational chemistry research so that it would be easy to analyze
large sets of output files named after the parameter used::

    $ ls *.out
    mode1000.35.out mode1243.34.out mode744.43.out mode943.54.out

(Obviously, in reality there would be more files, but you get the idea.)  Notice
that the shell sorts in lexicographical order.  This is the behavior of programs like
``find`` as well as ``ls``.  The problem is in passing these files to an
analysis program that causes them not to appear in numerical order, which can lead
to bad analysis.  To remedy this, use ``natsort``::

    # This won't get you what you want
    $ foo *.out
    # This will sort naturally
    $ natsort *.out
    mode744.43.out
    mode943.54.out
    mode1000.35.out 
    mode1243.34.out
    $ natsort *.out | xargs foo

You can also filter out numbers using the ``natsort`` command-line script::

    $ natsort *.out -f 900 1100 # Select only numbers between 900-1100
    mode943.54.out
    mode1000.35.out 

If needed, you can exclude specific numbers::

    $ natsort *.out -e 1000.35 # Exclude 1000.35 from search
    mode744.43.out
    mode943.54.out
    mode1243.34.out

For other options, use ``natsort --help``.  In general, the other options mirror
the ``natsorted`` API.

It is also helpful to note that ``natsort`` accepts pipes. 

Note to users of the ``natsort`` shell script from < v. 3.1.0
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

The ``natsort`` shell script options and implementation for version 3.1.0 has
changed slightly.  Options relating to interpreting input as file or directory
paths have been removed, and internally the input is no longer treated as file
paths.  In most situations, this should not give different results, but in
some unique cases it may.  Feel free to contact me if this ruins your work flow.

Author
------

Seth M. Morton

History
-------

06-28-2014 v. 3.3.0
'''''''''''''''''''

    - Added a 'versorted' method for more convenient sorting of versions.
    - Updated command-line tool --number_type option with 'version' and 'ver'
      to make it more clear how to sort version numbers.
    - Moved unit-testing mechanism from being docstring-based to actual unit tests
      in actual functions.

      - This has provided the ability determine the coverage of the unit tests (99%).
      - This also makes the pydoc documentation a bit more clear.

    - Made docstrings for public functions mirror the README API.
    - Connected natsort development to Travis-CI to help ensure quality releases.

06-20-2014 v. 3.2.1
'''''''''''''''''''

    - Re-"Fixed" unorderable types issue on Python 3.x - this workaround
      is for when the problem occurs in the middle of the string.

05-07-2014 v. 3.2.0
'''''''''''''''''''

    - "Fixed" unorderable types issue on Python 3.x with a workaround that
      attempts to replicate the Python 2.x behavior by putting all the numbers
      (or strings that begin with numbers) first.
    - Now explicitly excluding __pycache__ from releases by adding a prune statement
      to MANIFEST.in.

05-05-2014 v. 3.1.2
'''''''''''''''''''

    - Added setup.cfg to support universal wheels.
    - Added Python 3.0 and Python 3.1 as requiring the argparse module.

03-01-2014 v. 3.1.1
'''''''''''''''''''

    - Added ability to sort lists of lists.
    - Cleaned up import statements.

01-20-2014 v. 3.1.0
'''''''''''''''''''

    - Added the ``signed`` and ``exp`` options to allow finer tuning of the sorting
    - Entire codebase now works for both Python 2 and Python 3 without needing to run
      ``2to3``.
    - Updated all doctests.
    - Further simplified the ``natsort`` base code by removing unneeded functions.
    - Simplified documentation where possible.
    - Improved the shell script code

        - Made the documentation less "path"-centric to make it clear it is not just
          for sorting file paths.
        - Removed the filesystem-based options because these can be achieved better
          though a pipeline.
        - Added doctests.
        - Added new options that correspond to ``signed`` and ``exp``.
        - The user can now specify multiple numbers to exclude or multiple ranges
          to filter by.

10-01-2013 v. 3.0.2
'''''''''''''''''''

    - Made float, int, and digit searching algorithms all share the same base function.
    - Fixed some outdated comments.
    - Made the ``__version__`` variable available when importing the module.

8-15-2013 v. 3.0.1
''''''''''''''''''

    - Added support for unicode strings.
    - Removed extraneous ``string2int`` function.
    - Fixed empty string removal function.

7-13-2013 v. 3.0.0
''''''''''''''''''

    - Added a ``number_type`` argument to the sorting functions to specify how
      liberal to be when deciding what a number is.
    - Reworked the documentation.

6-25-2013 v. 2.2.0
''''''''''''''''''

    - Added ``key`` attribute to ``natsorted`` and ``index_natsorted`` so that
      it mimics the functionality of the built-in ``sorted``
    - Added tests to reflect the new functionality, as well as tests demonstrating
      how to get similar functionality using ``natsort_key``.

12-5-2012 v. 2.1.0
''''''''''''''''''

    - Reorganized package.
    - Now using a platform independent shell script generator (entry_points
      from distribute).
    - Can now execute natsort from command line with ``python -m natsort``
      as well.

11-30-2012 v. 2.0.2
'''''''''''''''''''

    - Added the use_2to3 option to setup.py.
    - Added distribute_setup.py to the distribution.
    - Added dependency to the argparse module (for python2.6).

11-21-2012 v. 2.0.1
'''''''''''''''''''

    - Reorganized directory structure.
    - Added tests into the natsort.py file iteself.

11-16-2012, v. 2.0.0
''''''''''''''''''''

    - Updated sorting algorithm to support floats (including exponentials) and
      basic version number support.
    - Added better README documentation.
    - Added doctests.
