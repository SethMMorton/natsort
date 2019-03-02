## 6.0.0 - 02-04-2019

 - Drop support for Python 2.6 and 3.3 (thanks @jdufresne) (issue #70)
 - Remove deprecated APIs (kwargs `number_type`, `signed`, `exp`, `as_path`,
     `py3_safe`; enums `ns.TYPESAFE`, `ns.DIGIT`, `ns.VERSION`; functions `versorted`,
     `index_versorted`) (issue #81)
 - Remove `pipenv` as a dependency for building (issue #86)
 - Simply Travis-CI configuration (thanks @jdufresne) (issue #88)
 - Fix README rendering in PyPI (thanks @altendky) (issue #89)

## 5.5.0 - 11-18-2018

 - Formally deprecated old or misleading APIs (issue #83)
 - Documentation, packaging, and CI cleanup (thanks @jdufresne) (issues #69, #71-#80)
 - Consolidate API documentation into a single page (issue #82)
 - Add a `CHANGELOG.rst` to the top-level of the repository (issue #85)
 - Add back support for very old versions of setuptools (issue #84)

## 5.4.1 - 09-09-2018

 - Fix error in a newly added test (issues #65, #67)
 - Changed code format and quality checking infrastructure (issue #68)

## 5.4.0 - 09-06-2018

 - Re-expose `natsort_key` as "public" and remove the associated `DepricationWarning`
 - Add better developer documentation
 - Refactor tests (issue #66)
 - Bump allowed [`fastnumbers`](https://github.com/SethMMorton/fastnumbers) version

## 5.3.3 - 07-07-2018

 - Update docs with a FAQ and quick how-it-works (issue #60)
 - Fix a `StopIteration` error in the testing code
 - Enable Python 3.7 support in Travis-CI (issue #61)

## 5.3.2 - 05-17-2018

 - Fix bug that prevented install on old versions of `setuptools` (issues #55, #56)
 - Revert layout from `src/natsort/` back to `natsort/` to make user
      testing simpler (issues #57, #58)

## 5.3.1 - 05-14-2018

 - No bugfixes or features, just infrastructure and installation updates
 - Move to defining dependencies with `Pipfile`
 - Development layout is now `src/natsort/` instead of `natsort/`
 - Add bumpversion infrastructure
 - Extras can be installed by "[]" notation

## 5.3.0 - 04-20-2018

 - Fix bug in assessing [`fastnumbers`](https://github.com/SethMMorton/fastnumbers)
     version at import-time (thanks @hholzgra) (issues #51, #53)
 - Add ability to consider unicode-decimal numbers as numbers (issues #52, #54)

## 5.2.0 - 02-14-2018

 - Add `ns.NUMAFTER` to cause numbers to be placed after non-numbers (issues #48, #49)
 - Add `natcmp` function (Python 2 only) (thanks @rinslow) (issue #47)

## 5.1.1 - 11-11-2017

 - Added additional unicode number support for Python 3.7
 - Added information on how to install and test (issue #46)

## 5.1.0 - 08-19-2017

 - Fixed `StopIteration` warning on Python 3.6+ (thanks @lykinsbd) (issues #42, #43)
 - All Unicode input is now normalized (issue #44, #45)

## 5.0.3 - 04-30-2017

 - Improved development infrastructure
 - Migrated documentation to ReadTheDocs

## 5.0.2 - 01-02-2017

 - Added additional unicode number support for Python 3.6
 - Renamed several internal functions and variables to improve clarity
 - Improved documentation examples
 - Added a "how does it work?" section to the documentation

## 5.0.1 - 06-04-2016

 - The `ns` enum attributes can now be imported from the top-level
      namespace
 - Fixed a bug with the `from natsort import *` mechanism
 - Fixed bug with using `natsort` with `python -OO` (issues #38, #39)

## 5.0.0 - 05-08-2016

 - `ns.LOCALE`/`humansorted` now accounts for thousands separators (issue #36)
 - Refactored entire codebase to be more functional (as in use functions as
      units). Previously, the code was rather monolithic and difficult to follow. The
      goal is that with the code existing in smaller units, contributing will
      be easier (issue #37)
 - Deprecated `ns.TYPESAFE` option as it is now always on (due to a new
      iterator-based algorithm, the typesafe function is now cheap)
 - Increased speed of execution (came for free with the new functional approach
      because the new factory function paradigm eliminates most `if` branches
      during execution). For the most cases, the code is 30-40% faster than version 4.0.4.
      If using `ns.LOCALE` or `humansorted`, the code is 1100% faster than version 4.0.4
 - Improved clarity of documentaion with regards to locale-aware sorting
 - Added a new `chain_functions` function for convenience in creating
      a complex user-given `key` from several existing functions

## 4.0.4 - 11-01-2015

 - Improved coverage of unit tests
 - Unit tests use new and improved hypothesis library
 - Fixed compatibility issues with Python 3.5

## 4.0.3 - 06-25-2015

 - Fixed bad install on last release (sorry guys!) (issue #30)

## 4.0.2 - 06-24-2015

 - Added back Python 2.6 and Python 3.2 compatibility. Unit testing is now
      performed for these versions (thanks @dpetzold) (issue #29)
 - Consolidated under-the-hood compatibility functionality

## 4.0.1 - 06-04-2015

 - Added support for sorting NaN by internally converting to -Infinity
      or +Infinity (issue #27)

## 4.0.0 - 05-17-2015

 - Made default behavior of `natsort` search for unsigned ints,
      rather than signed floats. This is a backwards-incompatible
      change but in 99% of use cases it should not require any
      end-user changes (issue #20)
 - Improved handling of locale-aware sorting on systems where the
      underlying locale library is broken (issue #34))
 - Greatly improved all unit tests by adding the `hypothesis` library

## 3.5.6 - 04-06-2015

 - Added `UNGROUPLETTERS` algorithm to get the case-grouping behavior of
      an ordinal sort when using `LOCALE` (issue #23)
 - Added convenience functions `decoder`, `as_ascii`, and `as_utf8` for
      dealing with bytes types

## 3.5.5 - 04-04-2015

 - Added `realsorted` and `index_realsorted` functions for
      forward-compatibility with >= 4.0.0
 - Made explanation of when to use `TYPESAFE` more clear in the docs

## 3.5.4 - 04-02-2015

 - Fixed bug where a `TypeError` was raised if a string containing a leading
      number was sorted with alpha-only strings when `LOCALE` is used (issue #22)

## 3.5.3 - 03-26-2015

 - Fixed bug where `--reverse-filter` option in shell script was not
      getting checked for correctness
 - Documentation updates to better describe locale bug, and illustrate
      upcoming default behavior change
 - Internal improvements, including making test suite more granular

## 3.5.2 - 01-13-2015

 - Enhancement that will convert a `pathlib.Path` object to a `str` if
      `ns.PATH` is enabled (issue #16)

## 3.5.1 - 09-25-2014

 - Fixed bug that caused list/tuples to fail when using `ns.LOWECASEFIRST`
      or `ns.IGNORECASE` (issue #15)
 - Refactored modules so that only the public API was in `natsort.py` and
      `ns_enum.py`
 - Refactored all import statements to be absolute, not relative


## 3.5.0 - 09-02-2014

 - Added the `alg` argument to the `natsort` functions.  This argument
      accepts an enum that is used to indicate the options the user wishes
      to use.  The `number_type`, `signed`, `exp`, `as_path`, and `py3_safe`
      options are being deprecated and will become (undocumented)
      keyword-only options in `natsort` version 4.0.0
 - The user can now modify how `natsort` handles the case of non-numeric
      characters (issue #14)
 - The user can now instruct `natsort` to use locale-aware sorting, which
      allows `natsort` to perform true "human sorting" (issue #14)
 - The `humansorted` convenience function as a convenience to locale-aware sorting
 - Updated shell script with locale functionality

## 3.4.1 - 08-12-2014

 - `natsort` will now use the [`fastnumbers`](https://github.com/SethMMorton/fastnumbers)
      module if it is installed. This gives up to an extra 30% boost in speed over
      the previous performance enhancements
 - Made documentation point to more `natsort` resources, and also added a
      new example in the examples section

## 3.4.0 - 07-19-2014

 - Fixed a bug that caused user's options to the 'natsort_key' to not be
      passed on to recursive calls of 'natsort_key' (issue #12)
 - Added a `natsort_keygen` function that will generate a wrapped version
      of `natsort_key` that is easier to call.  `natsort_key` is now set to
      deprecate at natsort version 4.0.0
 - Added an `as_path` option to `natsorted` & co. that will try to treat
      input strings as filepaths. This will help yield correct results for
      OS-generated inputs like
      `['/p/q/o.x', '/p/q (1)/o.x', '/p/q (10)/o.x', '/p/q/o (1).x']` (issue #3)
 - Massive performance enhancements for string input (1.8x-2.0x), at the expense
      of reduction in speed for numeric input (~2.0x) - note that sorting numbers\
      still only takes 0.6x the time of sorting strings
 - Added the `order_by_index` function to help in using the output of
      `index_natsorted` and `index_versorted`
 - Added the `reverse` option to `natsorted` & co. to make it's API more
      similar to the builtin 'sorted'
 - Added more unit tests
 - Added auxillary test code that helps in profiling and stress-testing
 - Reworked the documentation, moving most of it to PyPI's hosting platform
 - Added support for coveralls.io
 - Entire codebase is now PyFlakes and PEP8 compliant

## 3.3.0 - 06-28-2014

 - Added a `versorted` method for more convenient sorting of versions (issue #11)
 - Updated command-line tool `--number_type` option with 'version' and 'ver'
      to make it more clear how to sort version numbers
 - Moved unit-testing mechanism from being docstring-based to actual unit tests
      in actual functions (issue #10)
 - Added unit test coverage (99%)
 - Made docstrings for public functions mirror the README API
 - Connected natsort development to Travis-CI to help ensure quality releases

## 3.2.1 - 06-20-2014

 - Re-"Fixed" unorderable types issue on Python 3.x - this workaround
      is for when the problem occurs in the middle of the string (issue #7 again)

## 3.2.0 - 05-07-2014

 - "Fixed" unorderable types issue on Python 3.x with a workaround that
      attempts to replicate the Python 2.x behavior by putting all the numbers
      (or strings that begin with numbers) first (issue #7)
 - Now explicitly excluding `__pycache__` from releases by adding a prune statement
      to MANIFEST.in

## 3.1.2 - 05-05-2014

 - Added setup.cfg to support universal wheels (issue #6)
 - Added Python 3.0 and Python 3.1 as requiring the argparse module

## 3.1.1 - 03-01-2014

 - Added ability to sort lists of lists (issue #5)
 - Cleaned up import statements

## 3.1.0 - 01-20-2014

 - Added the `signed` and `exp` options to allow finer tuning of the sorting
 - Entire codebase now works for both Python 2 and Python 3 without needing to run
      `2to3`
 - Updated all doctests
 - Further simplified the `natsort` base code by removing unneeded functions.
 - Simplified documentation where possible
 - Improved the shell script code
 - Made the shell script documentation less "path"-centric to make it clear it is not just
          for sorting file paths
 - Removed the shell script filesystem-based options because these can be achieved better
          though a pipeline
 - Added doctests
 - Added new options that correspond to `signed` and `exp`
 - The user can now specify multiple numbers to exclude or multiple ranges
          by which to filter

## 3.0.2 - 10-01-2013

 - Made float, int, and digit searching algorithms all share the same base function
 - Fixed some outdated comments
 - Made the `__version__` variable available when importing the module

## 3.0.1 - 8-15-2013

 - Added support for unicode strings (issue #2)
 - Removed extraneous `string2int` function
 - Fixed empty string removal function

## 3.0.0 - 7-13-2013

 - Added a `number_type` argument to the sorting functions to specify how
      liberal to be when deciding what a number is
 - Reworked the documentation

## 2.2.0 - 6-25-2013

 - Added `key` attribute to `natsorted` and `index_natsorted` so that
      it mimics the functionality of the built-in `sorted` (issue #1)
 - Added tests to reflect the new functionality, as well as tests demonstrating
      how to get similar functionality using `natsort_key`

## 2.1.0 - 12-5-2012

 - Reorganized package
 - Now using a platform independent shell script generator (entry_points from distribute)
 - Can now execute natsort from command line with `python -m natsort` as well

## 2.0.2 - 11-30-2012

 - Added the use_2to3 option to setup.py
 - Added distribute_setup.py to the distribution
 - Added dependency to the argparse module (for python2.6)

## 2.0.1 - 11-21-2012

 - Reorganized directory structure
 - Added tests into the natsort.py file iteself

## 2.0.0 - 11-16-2012

 - Updated sorting algorithm to support floats (including exponentials) and
      basic version number support
 - Added better README documentation
 - Added doctests
