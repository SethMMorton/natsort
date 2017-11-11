.. default-domain:: py
.. module:: natsort

The :mod:`natsort` module
=========================

Simple yet flexible natural sorting in Python.

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.org/project/natsort/
    - Documentation: http://natsort.readthedocs.io/

      - :ref:`Examples and Recipes <examples>`
      - :ref:`How Does Natsort Work? <howitworks>`
      - :ref:`API <api>`
      - **NOTE**: The old documentation at pythonhosted.org has been taken down
        with no redirects. Please see
        `this post <https://opensource.stackexchange.com/q/5941/8999>`_ for an
        explanation into why.

    - Optional Dependencies:

      - `fastnumbers <https://pypi.org/project/fastnumbers>`_ >= 0.7.1
      - `PyICU <https://pypi.org/project/PyICU>`_ >= 1.0.0

:mod:`natsort` is a general utility for sorting lists *naturally*; the definition
of "naturally" is not well-defined, but the most common definition is that numbers
contained within the string should be sorted as numbers and not as you would
other characters. If you need to present sorted output to a user, you probably
want to sort it naturally.

:mod:`natsort` was initially created for sorting scientific output filenames that
contained signed floating point numbers in the names. There was a lack of
algorithms out there that could perform a natural sort on `floats` but
plenty for `ints`; check out
`this StackOverflow question <http://stackoverflow.com/q/4836710/1399279>`_
and its answers and links therein,
`this ActiveState forum <http://code.activestate.com/recipes/285264-natural-string-sorting/>`_,
and of course `this great article on natural sorting <http://blog.codinghorror.com/sorting-for-humans-natural-sort-order/>`_
from CodingHorror.com for examples of what I mean.
:mod:`natsort` was created to fill in this gap, but has since expanded to handle
just about any definition of a number, as well as other sorting customizations.

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

:mod:`natsort` provides a function :func:`~natsorted` that helps sort lists
"naturally" ("naturally" is rather ill-defined, but in general it means
sorting based on meaning and not computer code point)..
Using :func:`~natsorted` is simple:

.. code-block:: python

    >>> from natsort import natsorted
    >>> a = ['2 ft 7 in', '1 ft 5 in', '10 ft 2 in', '2 ft 11 in', '7 ft 6 in']
    >>> natsorted(a)
    ['1 ft 5 in', '2 ft 7 in', '2 ft 11 in', '7 ft 6 in', '10 ft 2 in']

:func:`~natsorted` identifies numbers anywhere in a string and sorts them
naturally. Below are some other things you can do with :mod:`natsort`
(please see the :ref:`examples` for a quick start guide, or the :ref:`api`
for more details).

.. note::

    :func:`~natsorted` is designed to be a drop-in replacement for the built-in
    :func:`sorted` function. Like :func:`sorted`, :func:`~natsorted`
    `does not sort in-place`. To sort a list and assign the output to the
    same variable, you must explicitly assign the output to a variable:

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

This is where the non-numeric characters are ordered based on their meaning,
not on their ordinal value, and a locale-dependent thousands separator and decimal
separator is accounted for in the number.
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
the ``ns`` enum :class:`~natsort.ns`.

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

Generating a Reusable Sorting Key and Sorting In-Place
++++++++++++++++++++++++++++++++++++++++++++++++++++++

Under the hood, :func:`~natsorted` works by generating a custom sorting
key using :func:`~natsort_keygen` and then passes that to the built-in
:func:`sorted`. You can use the :func:`~natsort_keygen` function yourself to
generate a custom sorting key to sort in-place using the :meth:`list.sort`
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
section can also be applied to :func:`~natsort_keygen` through the *alg* keyword option.

Other Useful Things
+++++++++++++++++++

 - recursively descend into lists of lists
 - controlling the case-sensitivity (see :ref:`case_sort`)
 - sorting file paths correctly (see :ref:`path_sort`)
 - allow custom sorting keys (see :ref:`custom_sort`)

Shell script
------------

:mod:`natsort` comes with a shell script called :mod:`natsort`, or can also be called
from the command line with ``python -m natsort``. 

Requirements
------------

:mod:`natsort` requires Python version 2.6 or greater or Python 3.3 or greater.
It may run on (but is not tested against) Python 3.2.

Optional Dependencies
---------------------

fastnumbers
+++++++++++

The most efficient sorting can occur if you install the
`fastnumbers <https://pypi.org/project/fastnumbers>`_ package
(version >=0.7.1); it helps with the string to number conversions.
:mod:`natsort` will still run (efficiently) without the package, but if you need
to squeeze out that extra juice it is recommended you include this as a dependency.
:mod:`natsort` will not require (or check) that
`fastnumbers <https://pypi.org/project/fastnumbers>`_ is installed
at installation.

PyICU
+++++

It is recommended that you install `PyICU <https://pypi.org/project/PyICU>`_
if you wish to sort in a locale-dependent manner, see
http://natsort.readthedocs.io/en/master/locale_issues.html for an explanation why.

Installation and Testing
------------------------

To install :mod:`natsort`, it is simplest to use ``pip``::

    pip install natsort

You can also add the `requirements.txt` file; it will ensure that ``argparse`` is
installed for Python 2.6 but does nothing on any other Python version::

    pip install -rrequirements.txt natsort

If you want to install the optional dependencies ``fastnumbers`` and ``PyICU``,
add the `optional-requirements.txt` file::

    pip install -roptional-requirements.txt natsort

If you wish to run the tests, please note that :mod:`natsort` is NOT set-up to
support ``python setup.py test``. The preferred way to run the tests is
to use `tox <https://tox.readthedocs.io/en/latest/>`_. If you want to run unit
tests on (for example) Python 2.7, you can execute the following::

    pip install tox
    tox -e py27

This will install all the necessary dependencies to run the :mod:`natsort` test suite.
If you prefer not to use ``tox``, you can run the tests manually using
`pytest <https://docs.pytest.org/en/latest/>`_::

    pip install -rtesting-requirements.txt
    python -m pytest

