.. _changelog:

Changelog
---------

01-13-2015 v. 3.5.2
'''''''''''''''''''

    - Enhancement that will convert a 'pathlib.Path' object to a 'str' if
      'ns.PATH' is enabled.

09-25-2014 v. 3.5.1
'''''''''''''''''''

    - Fixed bug that caused list/tuples to fail when using 'ns.LOWECASEFIRST'
      or 'ns.IGNORECASE'.
    - Refactored modules so that only the public API was in natsort.py and
      ns_enum.py.
    - Refactored all import statements to be absolute, not relative.


09-02-2014 v. 3.5.0
'''''''''''''''''''

    - Added the 'alg' argument to the 'natsort' functions.  This argument
      accepts an enum that is used to indicate the options the user wishes
      to use.  The 'number_type', 'signed', 'exp', 'as_path', and 'py3_safe'
      options are being depreciated and will become (undocumented)
      keyword-only options in natsort version 4.0.0.
    - The user can now modify how 'natsort' handles the case of non-numeric
      characters.
    - The user can now instruct 'natsort' to use locale-aware sorting, which
      allows 'natsort' to perform true "human sorting".

      - The `humansorted` convenience function has been included to make this
        easier.

    - Updated shell script with locale functionality.

08-12-2014 v. 3.4.1
'''''''''''''''''''

    - 'natsort' will now use the 'fastnumbers' module if it is installed. This
      gives up to an extra 30% boost in speed over the previous performance
      enhancements.
    - Made documentation point to more 'natsort' resources, and also added a
      new example in the examples section.

07-19-2014 v. 3.4.0
'''''''''''''''''''

    - Fixed a bug that caused user's options to the 'natsort_key' to not be
      passed on to recursive calls of 'natsort_key'.
    - Added a 'natsort_keygen' function that will generate a wrapped version
      of 'natsort_key' that is easier to call.  'natsort_key' is now set to
      depreciate at natsort version 4.0.0.
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
'''''''''''''''''''

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
'''''''''''''''''''

    - Re-"Fixed" unorderable types issue on Python 3.x - this workaround
      is for when the problem occurs in the middle of the string.

05-07-2014 v. 3.2.0
'''''''''''''''''''

    - "Fixed" unorderable types issue on Python 3.x with a workaround that
      attempts to replicate the Python 2.x behavior by putting all the numbers
      (or strings that begin with numbers) first.
    - Now explicitly excluding __pycache__ from releases by adding a prune statement
      to MANIFEST.in.

05-05-2014 v. 3.1.2
'''''''''''''''''''

    - Added setup.cfg to support universal wheels.
    - Added Python 3.0 and Python 3.1 as requiring the argparse module.

03-01-2014 v. 3.1.1
'''''''''''''''''''

    - Added ability to sort lists of lists.
    - Cleaned up import statements.

01-20-2014 v. 3.1.0
'''''''''''''''''''

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
'''''''''''''''''''

    - Made float, int, and digit searching algorithms all share the same base function.
    - Fixed some outdated comments.
    - Made the ``__version__`` variable available when importing the module.

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

    - Reorganized package.
    - Now using a platform independent shell script generator (entry_points
      from distribute).
    - Can now execute natsort from command line with ``python -m natsort``
      as well.

11-30-2012 v. 2.0.2
'''''''''''''''''''

    - Added the use_2to3 option to setup.py.
    - Added distribute_setup.py to the distribution.
    - Added dependency to the argparse module (for python2.6).

11-21-2012 v. 2.0.1
'''''''''''''''''''

    - Reorganized directory structure.
    - Added tests into the natsort.py file iteself.

11-16-2012, v. 2.0.0
''''''''''''''''''''

    - Updated sorting algorithm to support floats (including exponentials) and
      basic version number support.
    - Added better README documentation.
    - Added doctests.
