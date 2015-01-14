# -*- coding: utf-8 -*-
"""This module defines the "ns" enum for natsort."""

from __future__ import (print_function, division,
                        unicode_literals, absolute_import)


class ns(object):
    """
    Enum to control the `natsort` algorithm.

    This class acts like an enum to control the `natsort` algorithm. The
    user may select several options simultaneously by or'ing the options
    together.  For example, to choose ``ns.INT``, `ns.PATH``, and
    ``ns.LOCALE``, you could do ``ns.INT | ns.LOCALE | ns.PATH``.

    Each option has a shortened 1- or 2-letter form.

    .. warning:: On some systems, the underlying C library that
                 Python's locale module uses is broken. On these
                 systems it is recommended that you install
                 `PyICU <https://pypi.python.org/pypi/PyICU>`_
                 if you wish to use `LOCALE`.
                 Please validate that `LOCALE` works as
                 expected on your target system, and if not you
                 should add
                 `PyICU <https://pypi.python.org/pypi/PyICU>`_
                 as a dependency.

    Attributes
    ----------
    FLOAT, F
        The default - parse numbers as floats.
    INT, I
        Tell `natsort` to parse numbers as ints.
    UNSIGNED, U
        Tell `natsort` to ignore any sign (i.e. "-" or "+") to the
        immediate left of a number.  It is the same as setting the old
        `signed` option to `False`.
    VERSION, V
        This is a shortcut for ``ns.INT | ns.UNSIGNED``, which is useful
        when attempting to sort version numbers.  It is the same as
        setting the old `number_type` option to `None`.
    DIGIT, D
        Same as `VERSION` above.
    NOEXP, N
        Tell `natsort` to not search for exponents as part of the number.
        For example, with `NOEXP` the number "5.6E5" would be interpreted
        as `5.6`, `"E"`, and `5`.  It is the same as setting the old `exp`
        option to `False`.
    PATH, P
        Tell `natsort` to interpret strings as filesystem paths, so they
        will be split according to the filesystem separator
        (i.e. ‘/’ on UNIX, ‘\’ on Windows), as well as splitting on the
        file extension, if any. Without this, lists of file paths like
        ``['Folder/', 'Folder (1)/', 'Folder (10)/']`` will not be sorted
        properly; 'Folder/' will be placed at the end, not at the front.
        It is the same as setting the old `as_path` option to `True`.
    LOCALE, L
        Tell `natsort` to be locale-aware when sorting strings (everything
        that was not converted to a number).  Your sorting results will vary
        depending on your current locale. Generally, the `GROUPLETTERS`
        option is not needed with `LOCALE` because the `locale` library
        groups the letters in the same manner (although you may still
        need `GROUPLETTERS` if there are numbers in your strings).
    IGNORECASE, IC
        Tell `natsort` to ignore case when sorting.  For example,
        ``['Banana', 'apple', 'banana', 'Apple']`` would be sorted as
        ``['apple', 'Apple', 'Banana', 'banana']``.
    LOWERCASEFIRST, LF
        Tell `natsort` to put lowercase letters before uppercase letters
        when sorting.  For example,
        ``['Banana', 'apple', 'banana', 'Apple']`` would be sorted as
        ``['apple', 'banana', 'Apple', 'Banana']`` (the default order
        would be ``['Apple', 'Banana', 'apple', 'banana']`` which is
        the order from a purely ordinal sort).
        Useless when used with `IGNORECASE`.
    GROUPLETTERS, G
        Tell `natsort` to group lowercase and uppercase letters together
        when sorting.  For example,
        ``['Banana', 'apple', 'banana', 'Apple']`` would be sorted as
        ``['Apple', 'apple', 'Banana', 'banana']``.
        Useless when used with `IGNORECASE`; use with `LOWERCASEFIRST`
        to reverse the order of upper and lower case.
    TYPESAFE, T
        Try hard to avoid "unorderable types" error on Python 3. It
        is the same as setting the old `py3_safe` option to `True`.

    Notes
    -----
    If using `LOCALE`, you may find that if you do not explicitly set
    the locale your results may not be as you expect... I have found that
    it depends on the system you are on. To do this is straightforward
    (in the below example I use 'en_US.UTF-8', but you should use your
    locale)::

        >>> import locale
        >>> # The 'str' call is only to get around a bug on Python 2.x
        >>> # where 'setlocale' does not expect unicode strings (ironic,
        >>> # right?)
        >>> locale.setlocale(locale.LC_ALL, str('en_US.UTF-8'))
        'en_US.UTF-8'

    It is preferred that you do this before importing `natsort`.
    If you use `PyICU <https://pypi.python.org/pypi/PyICU>`_ (see warning
    above) then you should not need to do this.

    """
    pass


# Sort algorithm "enum" values.
_nsdict = {'FLOAT': 0,           'F': 0,
           'INT': 1,             'I': 1,
           'UNSIGNED': 2,        'U': 2,
           'VERSION': 3,         'V': 3,  # Shortcut for INT | UNSIGNED
           'DIGIT': 3,           'D': 3,  # Shortcut for INT | UNSIGNED
           'NOEXP': 4,           'N': 4,
           'PATH': 8,            'P': 8,
           'LOCALE': 16,         'L': 16,
           'IGNORECASE': 32,     'IC': 32,
           'LOWERCASEFIRST': 64, 'LF': 64,
           'GROUPLETTERS': 128,  'G': 128,
           'TYPESAFE': 1024,     'T': 1024,
           }
# Populate the ns class with the _nsdict values.
for x, y in _nsdict.items():
    setattr(ns, x, y)
