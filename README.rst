natsort
=======

Natural sorting for python.  ``natsort`` requires 2.7 or (2.6 with the argparse
module).  It has not been tested against python 3 or greater, but it should
automatically convert the code to work with python 3 when you install it (let
me know if you have issues with this).

Synopsis
--------

The ``natsort`` package provides a key helps sorts lists "naturally"; that is
it sorts alphabetically and numerically, and not by ASCII.  It provides support
for ints and floats (including negatives and exponental notation) and basic
support for sorting version numbers (1.2.3, no letters).

When you try to sort a list of strings that contain numbers, the normal python
sort algorithm sorts by ASCII, so you might not get the results that you
expect::

    >>> a = ['a2', 'a8', 'a7', 'a5', 'a9', 'a1', 'a4', 'a10', 'a3', 'a6']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']

Notice that it has the order ('1', '10', '2')?  This is because the list is
being sorted in ASCII order, which sorts numbers like you would letters (i.e.
'a', 'at', 'b').  It would be better if you had a sorting algorithm that
recognized numbers as numbers and treated them like numbers, not letters.  This
is where ``natsort`` comes in::

    >>> from natsort import natsorted
    >>> a = ['a2', 'a8', 'a7', 'a5', 'a9', 'a1', 'a4', 'a10', 'a3', 'a6']
    >>> natsorted(a)
    ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10']

``natsort`` identifies the numbers and sorts them separately from the numbers.
It not only works on integers, but on floats as well (even in exponential
notation!)::

    >>> a = ['a50', 'a51.', 'a50.4', 'a5.034e1', 'a50.300']
    >>> sorted(a)
    ['a5.034e1', 'a50', 'a50.300', 'a50.4', 'a51.']
    >>> natsorted(a)
    ['a50', 'a50.300', 'a5.034e1', 'a50.4', 'a51.']

Last, ``natsort`` can also handle version numbers appropriately, provided they
are in the format "M.m.p" where M=major version number, m=minor version number,
and p=patch.  The patch can be just a number, or can also be a number followed
by a letter.  You must include the patch, otherwise ``natsort`` will think it
is a float::

    >>> a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    >>> sorted(a)
    ['1.10.1', '1.11', '1.11.4', '1.9.9a', '1.9.9b']
    >>> natsorted(a)
    ['1.9.9a', '1.9.9b', '1.10.1', '1.11.4', '1.11']
    >>> # If you had used 1.11.0 instead of 1.11 this would work properly
    >>> a = ['1.9.9a', '1.11.0', '1.9.9b', '1.11.4', '1.10.1']
    >>> natsorted(a)
    ['1.9.9a', '1.9.9b', '1.10.1', '1.11.0', '1.11.4']

``natsort`` is not necessarily optimized for speed, but it is designed to be as
flexible as possible.

API
---

The ``natsort`` package provides three functions: ``natsort_key``,
``natsorted``, and ``index_natsorted``.

natsort_key
'''''''''''

Using ``natsort_key`` is just like any other sorting key in python::

    >>> from natsort import natsort_key
    >>> a = ['num3', 'num5', 'num2']
    >>> a.sort(key=natsort_key)
    >>> a
    ['num2', 'num3', 'num5']

natsorted
'''''''''

``natsorted`` is simply a wrapper for ``sorted(list, key=natsort_key)``::

    >>> from natsort import natsorted
    >>> a = ['num3', 'num5', 'num2']
    >>> natsorted(a)
    ['num2', 'num3', 'num5']

index_natsorted
'''''''''''''''

Use ``index_natsorted`` if you want to sort multiple lists by the sorting of
one list::

    >>> from natsort import index_natsorted
    >>> a = ['num3', 'num5', 'num2']
    >>> b = ['foo', 'bar', 'baz']
    >>> index = index_natsorted(a)
    >>> # Sort both lists by the sort order of a
    >>> a = [a[i] for i in index]
    >>> b = [b[i] for i in index]
    >>> a
    ['num2', 'num3', 'num5']
    >>> b
    ['baz', 'foo', 'bar']

Shell Script
------------

For your convenience, there is a natsort shell script supplied to you that
allows you to call natsort from the command-line.  ``natsort`` was written to
aid in computational chemistry researh so that it would be easy to analyze
large sets of output files named after the parameter used::

    $ ls *.out
    mode1000.35.out mode1243.34.out mode744.43.out mode943.54.out

(Obvously, in reality there would be more files, but you get the idea.)  Notice
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
