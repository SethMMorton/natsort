natsort
=======

Natural sorting for python.  ``natsort`` requires python version 2.6 or greater
(this includes python 3.x). To run version 2.6, the argparse module is
required.

``natsort`` comes with a shell script that is desecribed below.  You can
also execute ``natsort`` from the command line with ``python -m natsort``.

There exists another natural sorting package for python called 
`naturalsort <https://pypi.python.org/pypi/naturalsort>`_.  This package
does not take into account floats and negatives (which is the default behavior
of ``natsort``) and so may be preferred if you wish to only sort version numbers.

Problem Statement
-----------------

When you try to sort a list of strings that contain numbers, the normal python
sort algorithm sorts by ASCII, so you might not get the results that you
expect::

    >>> a = ['a2', 'a8', 'a7', 'a5', 'a9', 'a1', 'a4', 'a10', 'a3', 'a6']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']

Notice that it has the order ('1', '10', '2')?  This is because the list is
being sorted in ASCII order, which sorts numbers like you would letters (i.e.
'a', 'at', 'b').  It would be better if you had a sorting algorithm that
recognized numbers as numbers and treated them like numbers, not letters.

This is where ``natsort`` comes it: it provides a key that helps sorts lists
"naturally".  It provides support for ints and floats (including negatives and
exponental notation) or you can turn this off to support sort version numbers.

Synopsis
--------

Using ``natsort`` is simple::

    >>> from natsort import natsorted
    >>> a = ['a2', 'a8', 'a7', 'a5', 'a9', 'a1', 'a4', 'a10', 'a3', 'a6']
    >>> natsorted(a)
    ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10']

``natsort`` identifies the numbers and sorts them separately from letters.

You can also mix and match ``int``, ``float``, ``str``, and ``unicode`` types
when you sort::

    >>> a = ['4.5', 6, 2.3, u'5']
    >>> sorted(a)
    [2.3, 6, '4.5', u'5']
    >>> natsorted(a)
    [2.3, '4.5', u'5', 6]

The sorting algorithms
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

To achieve this, selecting this number type causes ``natsort`` to parse 
the string 'b-40.2' into ['b', -40.2].

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

To achieve this, selecting this number type causes ``natsort`` to parse 
the string 'b-40.2' into ['b', -40, '.', 2].

Sort by digits
++++++++++++++

The only difference between sorting by ints and sorting by digits is that
sorting by ints may take into account a negative sign, and sorting by digits
will not.  This may be an issue if you used a '-' as your separator before the
version numbers::

    >>> a = ['ver-2.9.9a', 'ver-1.11', 'ver-2.9.9b', 'ver-1.11.4', 'ver-1.10.1']
    >>> natsorted(a, number_type=int)
    ['ver-2.9.9a', 'ver-2.9.9b', 'ver-1.10.1', 'ver-1.11', 'ver-1.11.4']
    >>> natsorted(a, number_type=None)
    ['ver-1.10.1', 'ver-1.11', 'ver-1.11.4', 'ver-2.9.9a', 'ver-2.9.9b']

To achieve this, selecting this number type causes ``natsort`` to parse 
the string 'b-40.2' into ['b-', 40, '.', 2].

Using a sorting key
'''''''''''''''''''

Like the builtin ``sorted`` function, ``natsorted`` can accept a key so that 
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

The ``natsort`` package provides three functions: ``natsort_key``,
``natsorted``, and ``index_natsorted``.

natsorted
'''''''''

``natsort.natsorted`` (*sequence*, *key* = ``lambda x: x``, *number_type* = ``float``)

    sequence (*iterable*)
        The sequence to sort.

    key (*function*)
        A key used to determine how to sort each element of the sequence.

    number_type (``None``, ``float``, ``int``)
        The types of number to sort on: ``float`` searches for floating point numbers,
        ``int`` searches for integers, and ``None`` searches for digits (like integers 
        but does not take into account negative sign).

    returns
        The sorted sequence.

Use ``natsorted`` just like the builtin ``sorted``::

    >>> from natsort import natsorted
    >>> a = ['num3', 'num5', 'num2']
    >>> natsorted(a)
    ['num2', 'num3', 'num5']

natsort_key
'''''''''''

``natsort.natsort_key`` (value, *number_type* = ``float``)

    value
        The value used by the sorting algorithm

    number_type (``None``, ``float``, ``int``)
        The types of number to sort on: ``float`` searches for floating point numbers,
        ``int`` searches for integers, and ``None`` searches for digits (like integers 
        but does not take into account negative sign).

    returns
        The modified value with numbers extracted.

Using ``natsort_key`` is just like any other sorting key in python::

    >>> from natsort import natsort_key
    >>> a = ['num3', 'num5', 'num2']
    >>> a.sort(key=natsort_key)
    >>> a
    ['num2', 'num3', 'num5']

If you need to call ``natsort_key`` with the ``number_type`` argument, or get a special
attribute or item of each element of the sequence, the easiest way is to make a 
``lambda`` expression that calls ``natsort_key``::

    >>> from operator import itemgetter
    >>> a = [['num4', 'b'], ['num8', 'c'], ['num2', 'a']]
    >>> f = itemgetter(0)
    >>> a.sort(key=lambda x: natsort_key(f(x), number_type=int))
    >>> a
    [['num2', 'a'], ['num4', 'b'], ['num8', 'c']]

index_natsorted
'''''''''''''''

``natsort.index_natsorted`` (*sequence*, *key* = ``lambda x: x``, *number_type* = ``float``)

    sequence (*iterable*)
        The sequence to sort.

    key (*function*)
        A key used to determine how to sort each element of the sequence.

    number_type (``None``, ``float``, ``int``)
        The types of number to sort on: ``float`` searches for floating point numbers,
        ``int`` searches for integers, and ``None`` searches for digits (like integers 
        but does not take into account negative sign).

    returns
        The ordered indexes of the sequence.

Use ``index_natsorted`` if you want to sort multiple lists by the sorting of
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

Shell Script
------------

For your convenience, there is a ``natsort`` shell script supplied to you that
allows you to call ``natsort`` from the command-line.  ``natsort`` was written to
aid in computational chemistry research so that it would be easy to analyze
large sets of output files named after the parameter used::

    $ ls *.out
    mode1000.35.out mode1243.34.out mode744.43.out mode943.54.out

(Obviously, in reality there would be more files, but you get the idea.)  Notice
that the shell sorts in ASCII order.  This is the behavior of programs like
``find`` as well as ``ls``.  The problem is, when passing these files to an
analysis program causes them not to appear in numerical order, which can lead
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

For other options, use ``natsort --help``.

It is also helpful to note that ``natsort`` accepts pipes, and also will sort
each directory in a PATH independently of each other.  Files in the current
directory are listed before files in subdirectories.

Author
------

Seth M. Morton

History
-------

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

    - Reorganized package
    - Now using a platform independent shell script generator (entry_points
      from distribute)
    - Can now execute natsort from command line with ``python -m natsort``
      as well

11-30-2012 v. 2.0.2
'''''''''''''''''''

    - Added the use_2to3 option to setup.py
    - Added distribute_setup.py to the distribution
    - Added dependency to the argparse module (for python2.6)

11-21-2012 v. 2.0.1
'''''''''''''''''''

    - Reorganized directory structure
    - Added tests into the natsort.py file iteself

11-16-2012, v. 2.0.0
''''''''''''''''''''

    - Updated sorting algorithm to support floats (including exponentials) and
      basic version number support
    - Added better README documentation
    - Added doctests
