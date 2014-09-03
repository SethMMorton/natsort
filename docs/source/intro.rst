.. default-domain:: py
.. module:: natsort

The :mod:`natsort` module
=========================

Natural sorting for python. 

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.python.org/pypi/natsort
    - Documentation: http://pythonhosted.org//natsort/

:mod:`natsort` was initially created for sorting scientific output filenames that
contained floating point numbers in the names. There was a serious lack of
algorithms out there that could perform a natural sort on `floats` but
plenty for `ints`; check out
`this StackOverflow question <http://stackoverflow.com/q/4836710/1399279>`_
and its answers and links therein,
`this ActiveState forum <http://code.activestate.com/recipes/285264-natural-string-sorting/>`_,
and of course `this great article on natural sorting <http://blog.codinghorror.com/sorting-for-humans-natural-sort-order/>`_
from CodingHorror.com for examples of what I mean.
:mod:`natsort` was created to fill in this gap.  It has since grown
and can now sort version numbers (which seems to be the
most common use case based on user feedback) as well as some other nice features.

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

:mod:`natsort` provides a function :func:`~natsorted` that helps sort lists
"naturally", either as real numbers (i.e. signed/unsigned floats or ints),
or as versions.  Using :func:`~natsorted` is simple::

    >>> from natsort import natsorted
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a)
    ['a1', 'a2', 'a4', 'a9', 'a10']

:func:`~natsorted` identifies real numbers anywhere in a string and sorts them
naturally.

Sorting version numbers is just as easy with :func:`~versorted`::

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
Please see :ref:`bug_note` and the Installation section 
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

Please see the :ref:`examples` for a quick start guide, or the :ref:`api`
for more details.

Installation
------------

Installation of :mod:`natsort` is ultra-easy.  Simply execute from the
command line::

    easy_install natsort

or, if you have ``pip`` (preferred over ``easy_install``)::

    pip install natsort

Both of the above commands will download the source for you.

You can also download the source from http://pypi.python.org/pypi/natsort,
or browse the git repository at https://github.com/SethMMorton/natsort.

If you choose to install from source, you can unzip the source archive and
enter the directory, and type::

    python setup.py install

If you wish to run the unit tests, enter::

    python setup.py test

If you want to build this documentation, enter::

    python setup.py build_sphinx

:mod:`natsort` requires python version 2.6 or greater
(this includes python 3.x). To run version 2.6, 3.0, or 3.1 the 
`argparse <https://pypi.python.org/pypi/argparse>`_ module is required.

The most efficient sorting can occur if you install the 
`fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ package (it helps
with the string to number conversions.)  ``natsort`` will still run (efficiently)
without the package, but if you need to squeeze out that extra juice it is
recommended you include this as a dependency.  ``natsort`` will not require (or
check) that `fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ is installed.

On some systems, Python's ``locale`` library can be buggy (I have found this to be
the case on Mac OS X), so ``natsort`` will use
`PyICU <https://pypi.python.org/pypi/PyICU>`_ under the hood if it is installed
on your computer; this will give more reliable results. ``natsort`` will not
require (or check) that `PyICU <https://pypi.python.org/pypi/PyICU>`_ is installed
at installation.

:mod:`natsort` comes with a shell script called :mod:`natsort`, or can also be called
from the command line with ``python -m natsort``.  The command line script is
only installed onto your ``PATH`` if you don't install via a wheel.  There is
apparently a known bug with the wheel installation process that will not create
entry points.
