.. _changelog:

Changelog
---------

11-11-2017 v. 5.1.1
+++++++++++++++++++

    - Added additional unicode number support for Python 3.7.
    - Added information on how to install and test.

08-19-2017 v. 5.1.0
+++++++++++++++++++

    - Fixed ``StopIteration`` warning on Python 3.6+.
    - All Unicode input is now normalized.

04-30-2017 v. 5.0.3
+++++++++++++++++++

    - Improved development infrastructure.
    - Migrated documentation to ReadTheDocs.

01-02-2017 v. 5.0.2
+++++++++++++++++++

    - Added additional unicode number support for Python 3.6.
    - Renamed several internal functions and variables to improve clarity.
    - Improved documentation examples.
    - Added a "how does it work?" section to the documentation.

06-04-2016 v. 5.0.1
+++++++++++++++++++

    - The ``ns`` enum attributes can now be imported from the top-level
      namespace.
    - Fixed a bug with the ``from natsort import *`` mechanism.
    - Fixed bug with using ``natsort`` with ``python -OO``.

05-08-2016 v. 5.0.0
+++++++++++++++++++

    - ``ns.LOCALE``/``humansorted`` now accounts for thousands separators.
    - Refactored entire codebase to be more functional (as in use functions as
      units). Previously, the code was rather monolithic and difficult to follow. The
      goal is that with the code existing in smaller units, contributing will
      be easier.
    - Deprecated ``ns.TYPESAFE`` option as it is now always on (due to a new
      iterator-based algorithm, the typesafe function is now cheap).
    - Increased speed of execution (came for free with the new functional approach
      because the new factory function paradigm eliminates most ``if`` branches
      during execution).

      - For the most cases, the code is 30-40% faster than version 4.0.4.
      - If using ``ns.LOCALE`` or ``humansorted``, the code is 1100% faster than
        version 4.0.4.

    - Improved clarity of documentaion with regards to locale-aware sorting.
    - Added a new ``chain_functions`` function for convenience in creating
      a complex user-given ``key`` from several existing functions.

11-01-2015 v. 4.0.4
+++++++++++++++++++

    - Improved coverage of unit tests.
    - Unit tests use new and improved hypothesis library.
    - Fixed compatibility issues with Python 3.5

06-25-2015 v. 4.0.3
+++++++++++++++++++

    - Fixed bad install on last release (sorry guys!).

06-24-2015 v. 4.0.2
+++++++++++++++++++

    - Added back Python 2.6 and Python 3.2 compatibility. Unit testing is now
      performed for these versions.
    - Consolidated under-the-hood compatibility functionality.

06-04-2015 v. 4.0.1
+++++++++++++++++++

    - Added support for sorting NaN by internally converting to -Infinity
      or +Infinity

05-17-2015 v. 4.0.0
+++++++++++++++++++

    - Made default behavior of 'natsort' search for unsigned ints,
      rather than signed floats. This is a backwards-incompatible
      change but in 99% of use cases it should not require any
      end-user changes.
    - Improved handling of locale-aware sorting on systems where the
      underlying locale library is broken.
    - Greatly improved all unit tests by adding the hypothesis library.

04-06-2015 v. 3.5.6
+++++++++++++++++++

    - Added 'UNGROUPLETTERS' algorithm to get the case-grouping behavior of
      an ordinal sort when using 'LOCALE'.
    - Added convenience functions 'decoder', 'as_ascii', and 'as_utf8' for
      dealing with bytes types.

04-04-2015 v. 3.5.5
+++++++++++++++++++

    - Added 'realsorted' and 'index_realsorted' functions for
      forward-compatibility with >= 4.0.0.
    - Made explanation of when to use "TYPESAFE" more clear in the docs.

04-02-2015 v. 3.5.4
+++++++++++++++++++

    - Fixed bug where a 'TypeError' was raised if a string containing a leading
      number was sorted with alpha-only strings when 'LOCALE' is used.

03-26-2015 v. 3.5.3
+++++++++++++++++++

    - Fixed bug where '--reverse-filter' option in shell script was not
      getting checked for correctness.
    - Documentation updates to better describe locale bug, and illustrate
      upcoming default behavior change.
    - Internal improvements, including making test suite more granular.

01-13-2015 v. 3.5.2
+++++++++++++++++++

    - Enhancement that will convert a 'pathlib.Path' object to a 'str' if
      'ns.PATH' is enabled.

09-25-2014 v. 3.5.1
+++++++++++++++++++

    - Fixed bug that caused list/tuples to fail when using 'ns.LOWECASEFIRST'
      or 'ns.IGNORECASE'.
    - Refactored modules so that only the public API was in natsort.py and
      ns_enum.py.
    - Refactored all import statements to be absolute, not relative.


09-02-2014 v. 3.5.0
+++++++++++++++++++

    - Added the 'alg' argument to the 'natsort' functions.  This argument
      accepts an enum that is used to indicate the options the user wishes
      to use.  The 'number_type', 'signed', 'exp', 'as_path', and 'py3_safe'
      options are being deprecated and will become (undocumented)
      keyword-only options in natsort version 4.0.0.
    - The user can now modify how 'natsort' handles the case of non-numeric
      characters.
    - The user can now instruct 'natsort' to use locale-aware sorting, which
      allows 'natsort' to perform true "human sorting".

      - The `humansorted` convenience function has been included to make this
        easier.

    - Updated shell script with locale functionality.

08-12-2014 v. 3.4.1
+++++++++++++++++++

    - 'natsort' will now use the 'fastnumbers' module if it is installed. This
      gives up to an extra 30% boost in speed over the previous performance
      enhancements.
    - Made documentation point to more 'natsort' resources, and also added a
      new example in the examples section.

07-19-2014 v. 3.4.0
+++++++++++++++++++

    - Fixed a bug that caused user's options to the 'natsort_key' to not be
      passed on to recursive calls of 'natsort_key'.
    - Added a 'natsort_keygen' function that will generate a wrapped version
      of 'natsort_key' that is easier to call.  'natsort_key' is now set to
      deprecate at natsort version 4.0.0.
    - Added an 'as_path' option to 'natsorted' & co. that will try to treat
      input strings as filepaths. This will help yield correct results for
      OS-generated inputs like
      ``['/p/q/o.x', '/p/q (1)/o.x', '/p/q (10)/o.x', '/p/q/o (1).x']``.
    - Massive performance enhancements for string input (1.8x-2.0x), at the expense
      of reduction in speed for numeric input (~2.0x).

      - This is a good compromise because the most common input will be strings,
        not numbers, and sorting numbers still only takes 0.6x the time of sorting
        strings.  If you are sorting only numbers, you would use 'sorted' anyway.

    - Added the 'order_by_index' function to help in using the output of
      'index_natsorted' and 'index_versorted'.
    - Added the 'reverse' option to 'natsorted' & co. to make it's API more
      similar to the builtin 'sorted'.
    - Added more unit tests.
    - Added auxillary test code that helps in profiling and stress-testing.
    - Reworked the documentation, moving most of it to PyPI's hosting platform.
    - Added support for coveralls.io.
    - Entire codebase is now PyFlakes and PEP8 compliant.

06-28-2014 v. 3.3.0
+++++++++++++++++++

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
+++++++++++++++++++

    - Re-"Fixed" unorderable types issue on Python 3.x - this workaround
      is for when the problem occurs in the middle of the string.

05-07-2014 v. 3.2.0
+++++++++++++++++++

    - "Fixed" unorderable types issue on Python 3.x with a workaround that
      attempts to replicate the Python 2.x behavior by putting all the numbers
      (or strings that begin with numbers) first.
    - Now explicitly excluding __pycache__ from releases by adding a prune statement
      to MANIFEST.in.

05-05-2014 v. 3.1.2
+++++++++++++++++++

    - Added setup.cfg to support universal wheels.
    - Added Python 3.0 and Python 3.1 as requiring the argparse module.

03-01-2014 v. 3.1.1
+++++++++++++++++++

    - Added ability to sort lists of lists.
    - Cleaned up import statements.

01-20-2014 v. 3.1.0
+++++++++++++++++++

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
+++++++++++++++++++

    - Made float, int, and digit searching algorithms all share the same base function.
    - Fixed some outdated comments.
    - Made the ``__version__`` variable available when importing the module.

8-15-2013 v. 3.0.1
++++++++++++++++++

    - Added support for unicode strings.
    - Removed extraneous ``string2int`` function.
    - Fixed empty string removal function.

7-13-2013 v. 3.0.0
++++++++++++++++++

    - Added a ``number_type`` argument to the sorting functions to specify how
      liberal to be when deciding what a number is.
    - Reworked the documentation.

6-25-2013 v. 2.2.0
++++++++++++++++++

    - Added ``key`` attribute to ``natsorted`` and ``index_natsorted`` so that
      it mimics the functionality of the built-in ``sorted``
    - Added tests to reflect the new functionality, as well as tests demonstrating
      how to get similar functionality using ``natsort_key``.

12-5-2012 v. 2.1.0
++++++++++++++++++

    - Reorganized package.
    - Now using a platform independent shell script generator (entry_points
      from distribute).
    - Can now execute natsort from command line with ``python -m natsort``
      as well.

11-30-2012 v. 2.0.2
+++++++++++++++++++

    - Added the use_2to3 option to setup.py.
    - Added distribute_setup.py to the distribution.
    - Added dependency to the argparse module (for python2.6).

11-21-2012 v. 2.0.1
+++++++++++++++++++

    - Reorganized directory structure.
    - Added tests into the natsort.py file iteself.

11-16-2012, v. 2.0.0
++++++++++++++++++++

    - Updated sorting algorithm to support floats (including exponentials) and
      basic version number support.
    - Added better README documentation.
    - Added doctests.
