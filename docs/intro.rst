.. default-domain:: py
.. module:: natsort

The :mod:`natsort` module
=========================

Simple yet flexible natural sorting in Python.

    - Source Code: https://github.com/SethMMorton/natsort
    - Downloads: https://pypi.org/project/natsort/
    - Documentation: https://natsort.readthedocs.io/
    - Optional Dependencies:

      - `fastnumbers <https://pypi.org/project/fastnumbers>`_ >= 2.0.0
      - `PyICU <https://pypi.org/project/PyICU>`_ >= 1.0.0

**NOTE**: Please see the `Deprecation Schedule`_ section for changes in
:mod:`natsort` version 6.0.0 and in the upcoming version 7.0.0.

:mod:`natsort` is a general utility for sorting lists *naturally*; the definition
of "naturally" is not well-defined, but the most common definition is that numbers
contained within the string should be sorted as numbers and not as you would
other characters. If you need to present sorted output to a user, you probably
want to sort it naturally.

:mod:`natsort` was initially created for sorting scientific output filenames that
contained signed floating point numbers in the names. There was a lack of
algorithms out there that could perform a natural sort on `floats` but
plenty for `ints`; check out
`this StackOverflow question <https://stackoverflow.com/q/4836710/1399279>`_
and its answers and links therein,
`this ActiveState forum <https://code.activestate.com/recipes/285264-natural-string-sorting/>`_,
and of course `this great article on natural sorting <https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/>`_
from CodingHorror.com for examples of what I mean.
:mod:`natsort` was created to fill in this gap, but has since expanded to handle
just about any definition of a number, as well as other sorting customizations.

Quick Description
-----------------

When you try to sort a list of strings that contain numbers, the normal python
sort algorithm sorts lexicographically, so you might not get the results that you
expect:

.. code-block:: pycon

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

.. code-block:: pycon

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

    .. code-block:: pycon

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

Examples
--------

Sorting Versions
++++++++++++++++

:mod:`natsort` does not (and never has) actually *comprehend* version numbers.
It just so happens that the most common versioning schemes are designed to
work with standard natural sorting techniques; these schemes include
``MAJOR.MINOR``, ``MAJOR.MINOR.PATCH``, ``YEAR.MONTH.DAY``. If your data
conforms to a scheme like this, then it will work out-of-the-box with
``natsorted`` (as of ``natsort`` version >= 4.0.0):

.. code-block:: pycon

    >>> a = ['version-1.9', 'version-2.0', 'version-1.11', 'version-1.10']
    >>> natsorted(a)
    ['version-1.9', 'version-1.10', 'version-1.11', 'version-2.0']

If you need to versions that use a more complicated scheme, please see
:ref:`rc_sorting` for examples.

Sorting by Real Numbers (i.e. Signed Floats)
++++++++++++++++++++++++++++++++++++++++++++

This is useful in scientific data analysis and was
the default behavior of :func:`~natsorted` for :mod:`natsort`
version < 4.0.0. Use the :func:`~realsorted` function:

.. code-block:: pycon

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

.. code-block:: pycon

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

.. code-block:: pycon

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
the :class:`~natsort.ns` enum.

You can also add your own custom transformation functions with the ``key`` argument.
These can be used with ``alg`` if you wish:

.. code-block:: pycon

    >>> a = ['apple2.50', '2.3apple']
    >>> natsorted(a, key=lambda x: x.replace('apple', ''), alg=ns.REAL)
    ['2.3apple', 'apple2.50']

Sorting Mixed Types
+++++++++++++++++++

You can mix and match ``int``, ``float``, and ``str`` (or ``unicode``) types
when you sort:

.. code-block:: pycon

    >>> a = ['4.5', 6, 2.0, '5', 'a']
    >>> natsorted(a)
    [2.0, '4.5', '5', 6, 'a']
    >>> # On Python 2, sorted(a) would return [2.0, 6, '4.5', '5', 'a']
    >>> # On Python 3, sorted(a) would raise an "unorderable types" TypeError

Handling Bytes on Python 3
++++++++++++++++++++++++++

:mod:`natsort` does not officially support the `bytes` type on Python 3, but
convenience functions are provided that help you decode to `str` first:

.. code-block:: pycon

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

.. code-block:: pycon

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
 - automatic unicode normalization of input data
 - controlling the case-sensitivity (see :ref:`case_sort`)
 - sorting file paths correctly (see :ref:`path_sort`)
 - allow custom sorting keys (see :ref:`custom_sort`)

FAQ
---

How do I debug :func:`~natsorted`?
    The best way to debug :func:`~natsorted` is to generate a key using :func:`~natsort_keygen`
    with the same options being passed to :func:`~natsorted`. One can take a look at
    exactly what is being done with their input using this key - it is highly recommended
    to `look at this issue describing how to debug <https://github.com/SethMMorton/natsort/issues/13#issuecomment-50422375>`_
    for *how* to debug, and also to review the :ref:`howitworks` page for *why*
    :mod:`natsort` is doing that to your data.

    If you are trying to sort custom classes and running into trouble, please take a look at
    https://github.com/SethMMorton/natsort/issues/60. In short,
    custom classes are not likely to be sorted correctly if one relies
    on the behavior of ``__lt__`` and the other rich comparison operators in their
    custom class - it is better to use a ``key`` function with :mod:`natsort`, or
    use the :mod:`natsort` key as part of your rich comparison operator definition.

How *does* :mod:`natsort` work?
    If you don't want to read :ref:`howitworks`, here is a quick primer.

    :mod:`natsort` provides a :term:`key function` that can be passed to
    :meth:`list.sort` or :func:`sorted` in order to modify the default sorting
    behavior. This key is generated on-demand with the key generator
    :func:`natsort.natsort_keygen`. :func:`natsort.natsorted` is essentially a
    wrapper for the following code:

    .. code-block:: pycon

        >>> from natsort import natsort_keygen
        >>> natsort_key = natsort_keygen()
        >>> sorted(['1', '10', '2'], key=natsort_key)
        ['1', '2', '10']

    Users can further customize :mod:`natsort` sorting behavior with the ``key``
    and/or ``alg`` options (see details in the `Further Customizing Natsort`_
    section).

    The key generated by :func:`natsort.natsort_keygen` *always* returns a :class:`tuple`. It
    does so in the following way (*some details omitted for clarity*):

      1. Assume the input is a string, and attempt to split it into numbers and
         non-numbers using regular expressions. Numbers are then converted into
         either :class:`int` or :class:`float`.
      2. If the above fails because the input is not a string, assume the input
         is some other sequence (e.g. :class:`list` or :class:`tuple`), and recursively
         apply the key to each element of the sequence.
      3. If the above fails because the input is not iterable, assume the input
         is an :class:`int` or :class:`float`, and just return the input in a :class:`tuple`.

    Because a :class:`tuple` is always returned, a :exc:`TypeError` should not be common
    unless one tries to do something odd like sort an :class:`int` against a :class:`list`.

:mod:`natsort` gave me results I didn't expect, and it's a terrible library!
    Did you try to debug using the above advice? If so, and you still cannot figure out
    the error, then please `file an issue <https://github.com/SethMMorton/natsort/issues/new>`_.

Shell script
------------

:mod:`natsort` comes with a shell script called :mod:`natsort`, or can also be called
from the command line with ``python -m natsort``.

Requirements
------------

:mod:`natsort` requires Python version 2.7 or Python 3.4 or greater.

Optional Dependencies
---------------------

fastnumbers
+++++++++++

The most efficient sorting can occur if you install the
`fastnumbers <https://pypi.org/project/fastnumbers>`_ package
(version >=2.0.0); it helps with the string to number conversions.
:mod:`natsort` will still run (efficiently) without the package, but if you need
to squeeze out that extra juice it is recommended you include this as a dependency.
:mod:`natsort` will not require (or check) that
`fastnumbers <https://pypi.org/project/fastnumbers>`_ is installed
at installation.

PyICU
+++++

It is recommended that you install `PyICU <https://pypi.org/project/PyICU>`_
if you wish to sort in a locale-dependent manner, see :ref:`locale_issues` for
an explanation why.

Installation
------------

Use ``pip``!

.. code-block:: sh

    $ pip install natsort

If you want to install the `Optional Dependencies`_, you can use the
`"extras" notation <https://packaging.python.org/tutorials/installing-packages/#installing-setuptools-extras>`_
at installation time to install those dependencies as well - use ``fast`` for
`fastnumbers <https://pypi.org/project/fastnumbers>`_ and ``icu`` for
`PyICU <https://pypi.org/project/PyICU>`_.

.. code-block:: sh

    # Install both optional dependencies.
    $ pip install natsort[fast,icu]
    # Install just fastnumbers
    $ pip install natsort[fast]

How to Run Tests
----------------

Please note that :mod:`natsort` is NOT set-up to support ``python setup.py test``.

The recommended way to run tests is with `tox <https://tox.readthedocs.io/en/latest/>`_.
After installing ``tox``, running tests is as simple as executing the following in the
``natsort`` directory:

.. code-block:: sh

    $ tox

``tox`` will create virtual a virtual environment for your tests and install all the
needed testing requirements for you.  You can specify a particular python version
with the ``-e`` flag, e.g. ``tox -e py36``. Static analysis is done with ``tox -e flake8``.
You can see all available testing environments with ``tox --listenvs``.

If you do not wish to use ``tox``, you can install the testing dependencies with the
``dev-requirements.txt`` file and then run the tests manually using
`pytest <https://docs.pytest.org/en/latest/>`_.

.. code-block:: console

    $ pip install -r dev-requirements.txt
    $ python -m pytest

Note that above I invoked ``python -m pytest`` instead of just ``pytest`` - this is because
`the former puts the CWD on sys.path <https://docs.pytest.org/en/latest/usage.html#calling-pytest-through-python-m-pytest>`_.

How to Build Documentation
--------------------------

If you want to build the documentation for :mod:`natsort`, it is recommended to use ``tox``:

.. code-block:: console

    $ tox -e docs

This will place the documentation in ``build/sphinx/html``.  If you do not
which to use ``tox``, you can do the following:

.. code-block:: console

    $ pip install sphinx sphinx_rtd_theme
    $ python setup.py build_sphinx

Deprecation Schedule
--------------------

Dropping Python 2.7 Support
+++++++++++++++++++++++++++

:mod:`natsort` version 7.0.0 will drop support for Python 2.7.

The version 6.X branch will remain as a "long term support" branch where bug fixes
are applied so that users who cannot update from Python 2.7 will not be forced to
use a buggy :mod:`natsort` version. Once version 7.0.0 is released, new features
will not be added to version 6.X, only bug fixes.

Deprecated APIs
+++++++++++++++

In :mod:`natsort` version 6.0.0, the following APIs and functions were removed

 - ``number_type`` keyword argument (deprecated since 3.4.0)
 - ``signed`` keyword argument (deprecated since 3.4.0)
 - ``exp`` keyword argument (deprecated since 3.4.0)
 - ``as_path`` keyword argument (deprecated since 3.4.0)
 - ``py3_safe`` keyword argument (deprecated since 3.4.0)
 - ``ns.TYPESAFE`` (deprecated since version 5.0.0)
 - ``ns.DIGIT`` (deprecated since version 5.0.0)
 - ``ns.VERSION`` (deprecated since version 5.0.0)
 - :func:`~natsort.versorted` (discouraged since version 4.0.0, officially deprecated since version 5.5.0)
 - :func:`~natsort.index_versorted` (discouraged since version 4.0.0, officially deprecated since version 5.5.0)

In general, if you want to determine if you are using deprecated APIs you can run your
code with the following flag

.. code-block:: console

    $ python -Wdefault::DeprecationWarning my-code.py

By default :exc:`DeprecationWarnings` are not shown, but this will cause them to be shown.
Alternatively, you can just set the environment variable ``PYTHONWARNINGS`` to
"default::DeprecationWarning" and then run your code.

Dropped Pipenv for Development
++++++++++++++++++++++++++++++

:mod:`natsort` version 6.0.0 no longer uses `Pipenv <https://pipenv.readthedocs.io/en/latest/>`_
to install development dependencies.

Dropped Python 2.6 and 3.3 Support
++++++++++++++++++++++++++++++++++

:mod:`natsort` version 6.0.0 dropped support for Python 2.6 and Python 3.3.
