.. default-domain:: py
.. module:: natsort

The :mod:`natsort` module
=========================

Natural sorting for python. 

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.python.org/pypi/natsort
    - Documentation: http://pythonhosted.org/natsort/

      - `fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ >= 0.7.1
      - `PyICU <https://pypi.python.org/pypi/PyICU>`_ >= 1.0.0

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
expect:

.. code-block:: python

    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a4', 'a9']

Notice that it has the order ('1', '10', '2') - this is because the list is
being sorted in lexicographical order, which sorts numbers like you would
letters (i.e. 'b', 'ba', 'c').

:mod:`natsort` provides a function :func:`~natsorted` that helps sort lists
"naturally", either as real numbers (i.e. signed/unsigned floats or ints),
or as versions.  Using :func:`~natsorted` is simple:

.. code-block:: python

    >>> from natsort import natsorted
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a)
    ['a1', 'a2', 'a4', 'a9', 'a10']

:func:`~natsorted` identifies numbers anywhere in a string and sorts them
naturally. Here are some other things you can do with :mod:`natsort`
(please see the :ref:`examples` for a quick start guide, or the :ref:`api`
for more details).

Sorting Versions
++++++++++++++++

This is handled properly by default (as of :mod:`natsort` version >= 4.0.0):

.. code-block:: python

    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> natsorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']

If you need to sort release candidates, please see :ref:`rc_sorting` for
a useful hack.

Sorting by Real Numbers (i.e. Signed Floats)
++++++++++++++++++++++++++++++++++++++++++++

This is useful in scientific data analysis and was
the default behavior of :func:`~natsorted` for :mod:`natsort`
version < 4.0.0. Use the :func:`~realsorted` function:

.. code-block:: python

    >>> from natsort import realsorted, ns
    >>> a = ['num5.10', 'num-3', 'num5.3', 'num2']
    >>> natsorted(a)
    ['num2', 'num5.3', 'num5.10', 'num-3']
    >>> natsorted(a, alg=ns.REAL)
    ['num-3', 'num2', 'num5.10', 'num5.3']
    >>> realsorted(a)
    ['num-3', 'num2', 'num5.10', 'num5.3']

Locale-Aware Sorting (or "Human Sorting")
+++++++++++++++++++++++++++++++++++++++++

This is where the non-numeric characters are ordered based on their meaning,
not on their ordinal value, and a locale-dependent thousands separator
is accounted for in the number.
This can be achieved with the :func:`~humansorted` function:

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
    >>> humansorted(a)
    ['apple15', 'apple14,689', 'Apple', 'banana', 'Banana']

You may find you need to explicitly set the locale to get this to work
(as shown in the example).
Please see :ref:`locale_issues` and the Installation section 
below before using the :func:`~humansorted` function.

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

:mod:`natsort` does not officially support the `bytes` type on Python 3, but
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

All of the ``*sorted`` functions from the :mod:`natsort` are convenience functions
around the something similar to the following:

.. code-block:: python

    >>> from natsort import natsort_keygen
    >>> natsort_key = natsort_keygen()
    >>> a = ['a2', 'a9', 'a1', 'a4', 'a10']
    >>> natsorted(a) == sorted(a, key=natsort_key)
    True

You can use this key for your own use (such as passing to ``list.sort``).
You can also customize the key with the ``ns`` enum
(see :class:`~natsort.ns`).

Other Useful Things
+++++++++++++++++++

 - recursively descend into lists of lists
 - controlling the case-sensitivity (see :ref:`case_sort`)
 - sorting file paths correctly (see :ref:`path_sort`)
 - allow custom sorting keys (see :ref:`custom_sort`)

Installation
------------

Installation of :mod:`natsort` is ultra-easy.  Simply execute from the
command line::

    pip install natsort

You can also download the source from http://pypi.python.org/pypi/natsort,
or browse the git repository at https://github.com/SethMMorton/natsort.

If you choose to install from source, you can unzip the source archive and
enter the directory, and type::

    python setup.py install

If you wish to run the unit tests, enter::

    python setup.py test

If you want to build this documentation, enter::

    python setup.py build_sphinx

:mod:`natsort` requires Python version 2.6 or greater or Python 3.2 or greater.

The most efficient sorting can occur if you install the 
`fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ package (it helps
with the string to number conversions.)  ``natsort`` will still run (efficiently)
without the package, but if you need to squeeze out that extra juice it is
recommended you include this as a dependency.  ``natsort`` will not require (or
check) that `fastnumbers <https://pypi.python.org/pypi/fastnumbers>`_ is installed.

It is recommended that you install `PyICU <https://pypi.python.org/pypi/PyICU>`_
if you wisht to sort in a locale-dependent manner, see :ref:`locale_issues` for
an explanation why.

:mod:`natsort` comes with a shell script called :mod:`natsort`, or can also be called
from the command line with ``python -m natsort``.  The command line script is
only installed onto your ``PATH`` if you don't install via a wheel.  There is
apparently a known bug with the wheel installation process that will not create
entry points.
