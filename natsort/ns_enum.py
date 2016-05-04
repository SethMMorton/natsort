# -*- coding: utf-8 -*-
"""This module defines the "ns" enum for natsort."""
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)


class ns(object):
    """
    Enum to control the `natsort` algorithm.

    This class acts like an enum to control the `natsort` algorithm. The
    user may select several options simultaneously by or'ing the options
    together.  For example, to choose ``ns.INT``, ``ns.PATH``, and
    ``ns.LOCALE``, you could do ``ns.INT | ns.LOCALE | ns.PATH``.

    Each option has a shortened 1- or 2-letter form.

    .. warning:: On BSD-based systems (like Mac OS X), the underlying
                 C library that Python's locale module uses is broken.
                 On these systems it is recommended that you install
                 `PyICU <https://pypi.python.org/pypi/PyICU>`_
                 if you wish to use ``LOCALE``, especially if you need
                 to handle non-ASCII characters. If you are on one of
                 systems and get unexpected results, please try using
                 `PyICU <https://pypi.python.org/pypi/PyICU>`_ before
                 filing a bug report to ``natsort``.

    .. warning:: It is recommended that you recreate your key with
                 :func:`natsort_keygen` each time you change locale
                 if you use the ``ns.LOCALE`` option.

    Attributes
    ----------
    INT, I (default)
        The default - parse numbers as integers.
    FLOAT, F
        Tell `natsort` to parse numbers as floats.
    UNSIGNED, U (default)
        Tell `natsort` to ignore any sign (i.e. "-" or "+") to the immediate
        left of a number.  It is the same as setting the old `signed` option
        to `False`. This is the default.
    SIGNED, S
        Tell `natsort` to take into account any sign (i.e. "-" or "+")
        to the immediate left of a number.  It is the same as setting
        the old `signed` option to `True`.
    REAL, R
        This is a shortcut for ``ns.FLOAT | ns.SIGNED``, which is useful
        when attempting to sort real numbers.
    NOEXP, N
        Tell `natsort` to not search for exponents as part of the number.
        For example, with `NOEXP` the number "5.6E5" would be interpreted
        as `5.6`, `"E"`, and `5`.  It is the same as setting the old
        `exp` option to `False`.
    PATH, P
        Tell `natsort` to interpret strings as filesystem paths, so they
        will be split according to the filesystem separator
        (i.e. '/' on UNIX, '\\' on Windows), as well as splitting on the
        file extension, if any. Without this, lists of file paths like
        ``['Folder/', 'Folder (1)/', 'Folder (10)/']`` will not be
        sorted properly; 'Folder/' will be placed at the end, not at the
        front. It is the same as setting the old `as_path` option to
        `True`.
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
        Useless when used with `IGNORECASE`. Please note that if used
        with ``LOCALE``, this actually has the reverse effect and will
        put uppercase first (this is because ``LOCALE`` already puts
        lowercase first); you may use this to your advantage if you
        need to modify the order returned with ``LOCALE``.
    GROUPLETTERS, G
        Tell `natsort` to group lowercase and uppercase letters together
        when sorting.  For example,
        ``['Banana', 'apple', 'banana', 'Apple']`` would be sorted as
        ``['Apple', 'apple', 'Banana', 'banana']``.
        Useless when used with `IGNORECASE`; use with `LOWERCASEFIRST`
        to reverse the order of upper and lower case.
    CAPITALFIRST, C
        Only used when `LOCALE` is enabled. Tell `natsort` to put all
        capitalized words before non-capitalized words. This is essentially
        the inverse of `GROUPLETTERS`, and is the default Python sorting
        behavior without `LOCALE`.
    UNGROUPLETTERS, UG
        An alias for `CAPITALFIRST`.
    NANLAST, NL
        If an NaN shows up in the input, this instructs `natsort` to
        treat these as +Infinity and place them after all the other numbers.
        By default, an NaN be treated as -Infinity and be placed first.
    TYPESAFE, T
        Deprecated as of `natsort` version 5.0.0; this option is now
        a no-op because it is always true.
    VERSION, V
        Deprecated as of `natsort` version 5.0.0; this option is now
        a no-op because it is the default.
    DIGIT, D
        Same as `VERSION` above.

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
    # Following were previously now options but are now defaults.
    TYPESAFE         = T  = 0
    INT              = I  = 0
    VERSION          = V  = 0
    DIGIT            = D  = 0
    UNSIGNED         = U  = 0

    # The below are options. The values are stored as powers of two
    # so bitmasks can be used to extract the user's requested options.
    FLOAT            = F  = 1 << 0
    SIGNED           = S  = 1 << 1
    REAL             = R  = FLOAT | SIGNED
    NOEXP            = N  = 1 << 2
    PATH             = P  = 1 << 3
    LOCALE           = L  = 1 << 4
    IGNORECASE       = IC = 1 << 5
    LOWERCASEFIRST   = LF = 1 << 6
    GROUPLETTERS     = G  = 1 << 7
    UNGROUPLETTERS   = UG = 1 << 8
    CAPITALFIRST     = C  = UNGROUPLETTERS
    NANLAST          = NL = 1 << 9

    # The below are private options for internal use only.
    _NUMERIC_ONLY    = REAL | NOEXP
    _DUMB            = 1 << 31
