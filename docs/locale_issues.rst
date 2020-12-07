.. default-domain:: py
.. currentmodule:: natsort

.. _locale_issues:

Possible Issues with :func:`~natsort.humansorted` or ``ns.LOCALE``
==================================================================

Being Locale-Aware Means Both Numbers and Non-Numbers
-----------------------------------------------------

In addition to modifying how characters are sorted, ``ns.LOCALE`` will take
into account locale-dependent thousands separators (and locale-dependent
decimal separators if ``ns.FLOAT`` is enabled). This means that if you are in a
locale that uses commas as the thousands separator, a number like
``123,456`` will be interpreted as ``123456``.  If this is not what you want,
you may consider using ``ns.LOCALEALPHA`` which will only enable locale-aware
sorting for non-numbers (similarly, ``ns.LOCALENUM`` enables locale-aware
sorting only for numbers).

Regenerate Key With :func:`~natsort.natsort_keygen` After Changing Locale
-------------------------------------------------------------------------

When :func:`~natsort.natsort_keygen` is called it returns a key function that
hard-codes the provided settings. This means that the key returned when
``ns.LOCALE`` is used contains the settings specifed by the locale
*loaded at the time the key is generated*. If you change the locale,
you should regenerate the key to account for the new locale.

Corollary: Do Not Reuse :func:`~natsort.natsort_keygen` After Changing Locale
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

If you change locale, the old function will not work as expected.
The :mod:`locale` library works with a global state. When
:func:`~natsort.natsort_keygen` is called it does the best job that it can to
make the returned function as static as possible and independent of the global
state, but the :func:`locale.strxfrm` function must access this global state to
work; therefore, if you change locale and use ``ns.LOCALE`` then you should
discard the old key.

.. note:: If you use `PyICU`_ then you may be able to reuse keys after changing
          locale.

The :mod:`locale` Module From the StdLib Has Issues
---------------------------------------------------

:mod:`natsort` will use `PyICU`_ for :func:`~natsort.humansorted` or
``ns.LOCALE`` if it is installed. If not, it will fall back on the
:mod:`locale` library from the Python stdlib. If you do not have `PyICU`_
installed, please keep the following known problems and issues in mind.

.. note:: Remember, if you have `PyICU`_ installed you shouldn't need to worry
          about any of these.

Explicitly Set the Locale Before Using ``ns.LOCALE``
++++++++++++++++++++++++++++++++++++++++++++++++++++

I have found that unless you explicitly set a locale, the sorted order may not
be what you expect. Setting this is straightforward
(in the below example I use 'en_US.UTF-8', but you should use your
locale):

.. code-block:: pycon

    >>> import locale
    >>> locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    'en_US.UTF-8'

.. _bug_note:

The :mod:`locale` Module Is Broken on Mac OS X
++++++++++++++++++++++++++++++++++++++++++++++

It's not Python's fault, but the OS... the locale library for BSD-based systems
(of which Mac OS X is one) is broken. See the following links:

  - https://stackoverflow.com/questions/3412933/python-not-sorting-unicode-properly-strcoll-doesnt-help
  - https://bugs.python.org/issue23195
  - https://github.com/SethMMorton/natsort/issues/21 (contains instructons on installing)
  - https://stackoverflow.com/questions/33459384/unicode-character-not-in-range-when-calling-locale-strxfrm
  - https://github.com/SethMMorton/natsort/issues/34

Of course, installing `PyICU`_ fixes this, but if you don't want to or cannot
install this there is some hope.

    1. As of ``natsort`` version 4.0.0, ``natsort`` is configured
       to compensate for a broken ``locale`` library. When sorting non-numbers
       it will handle case as you expect, but it will still not be able to
       comprehend non-ASCII characters properly. Additionally, it has
       a built-in lookup table of thousands separators that are incorrect
       on OS X/BSD (but is possible it is not complete... please file an
       issue if you see it is not complete)
    2. Use "\*.ISO8859-1" locale (i.e. 'en_US.ISO8859-1') rather than
       "\*.UTF-8" locale. I have found that these have fewer issues than
       "UTF-8", but your mileage may vary.

.. _PyICU: https://pypi.org/project/PyICU
