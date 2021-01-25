Unreleased
---

[7.1.1] - 2021-01-24
---

### Changed
 - Use GitHub Actions instead of Travis-CI (issue #125)
 - No longer pin testing dependencies (issue #126)

### Fixed
 - Correct a minor typo ([@madphysicist](https://github.com/madphysicist), issue #127)

[7.1.0] - 2020-11-19
---

### Added
 - ``os_sorted``, ``os_sort_keygen``, and ``os_sort_key`` to better support
   sorting like the file browser on the current operating system - this
   closes the long-standing issue #41
 - Support for Python 3.9 ([@swt2c](https://github.com/swt2c), issue #119)

### Changed
 - MacOS unit tests run on native Python
 - Treate `None` like `NaN` internally to avoid `TypeError` (issue #117)
 - No longer fail tests every time a new Python version is released (issue #122)

### Fixed
 - Various typos, missing figures, and out-of-date information in the "How it works"
 - Fix typo in CHANGELOG ([@graingert](https://github.com/graingert), issue #113)
 - Updated "How it works" to account for Pandas updates
   ([@kuraga](https://github.com/kuraga), issue #116)

[7.0.1] - 2020-01-27
---

### Fixed
 - Bug where that caused incorrect sorting when using locales
   that have a `"."` character as the thousands separator.

[7.0.0] - 2020-01-08
---

### Added
 - Ability to deploy directly from TravisCI ([@hugovk](https://github.com/hugovk), issue #106)
 - Release checklist in `RELEASING.md` ([@hugovk](https://github.com/hugovk), issue #106)

### Changed
 - Updated auxillary shell scripts to be written in python, and added
   ability to call these from `tox`
 - Improved Travis-CI experience
 - Update testing dependency versions

### Removed
 - Support for Python 2

[6.2.0] - 2019-11-13
---

### Added
 - Support for Python 3.8 ([@hugovk](https://github.com/hugovk), issue #104)

### Changed
 - `index_natsorted` internally now uses tuples for index-element pairs
   instead of lists
 - Added a TOC to the README
 - Python 3.4 is no longer included in testing

### Fixed
 - Pin testing dependencies to prevent CI breaking due to third-party
   library changes

### Removed
 - Introduction page in documentation

[6.1.0] - 2019-11-09
---

### Added
 - Expose `numeric_regex_chooser` as a public function for ease in making
   key functions
 - Example in the documentation on how to sort numbers with units
 - Automated testing support for macos and Windows (issue #91)

### Changed
 - Update CHANGELOG format to style from https://keepachangelog.com/ (issue #92)

### Fixed
 - Removed dependency on `sudo` in TravisCI configuration ([@hugovk](https://github.com/hugovk), issue #99)
 - Documentation typos ([@jdufresne](https://github.com/jdufresne), issue #94) ([@cpburnz](https://github.com/cpburnz), issue #95)

[6.0.0] - 2019-02-04
---

### Changed
 - Simply Travis-CI configuration ([@jdufresne](https://github.com/jdufresne), issue #88)

### Fixed
 - Fix README rendering in PyPI ([@altendky](https://github.com/altendky), issue #89)

### Removed
 - Drop support for Python 2.6 and 3.3 ([@jdufresne](https://github.com/jdufresne), issue #70)
 - Remove deprecated APIs (kwargs `number_type`, `signed`, `exp`, `as_path`,
   `py3_safe`; enums `ns.TYPESAFE`, `ns.DIGIT`, `ns.VERSION`; functions `versorted`,
   `index_versorted`) (issue #81)
 - Remove `pipenv` as a dependency for building (issue #86)

[5.5.0] - 2018-11-18
---

### Added
 - `CHANGELOG.rst` to the top-level of the repository (issue #85)

### Changed
 - Documentation, packaging, and CI cleanup
   ([@jdufresne](https://github.com/jdufresne), issues #69, #71-#80)
 - Consolidate API documentation into a single page (issue #82)

### Deprecated
 - Formally deprecated old or misleading APIs (issue #83)

### Fixed
 - Add back support for very old versions of setuptools (issue #84)

[5.4.1] - 2018-09-09
---

### Changed
 - Code format and quality checking infrastructure (issue #68)

### Fixed
 - Error in a newly added test (issues #65, #67)

[5.4.0] - 2018-09-06
---

### Changed
 - Re-expose `natsort_key` as "public" and remove the associated `DeprecationWarning`
 - Better developer documentation
 - Refactor tests (issue #66)
 - Bump allowed [`fastnumbers`](https://github.com/SethMMorton/fastnumbers) version

[5.3.3] - 2018-07-07
---

### Added
 - Enable Python 3.7 support in Travis-CI (issue #61)

### Changed
 - Update docs with a FAQ and quick how-it-works (issue #60)

### Fixed
 - `StopIteration` error in the testing code


[5.3.2] - 2018-05-17
---

### Fixed
 - Bug that prevented install on old versions of `setuptools` (issues #55, #56)
 - Revert layout from `src/natsort/` back to `natsort/` to make user
   testing simpler (issues #57, #58)

[5.3.1] - 2018-05-14
---

### Added
 - [`bumpversion`](https://github.com/c4urself/bump2version) infrastructure
 - Extras can be installed by "[]" notation

### Changed
 - No bugfixes or features, just infrastructure and installation updates
 - Move to defining dependencies with `Pipfile`
 - Development layout is now `src/natsort/` instead of `natsort/`

[5.3.0] - 2018-04-20
---

### Added
 - Ability to consider unicode-decimal numbers as numbers (issues #52, #54)

### Fixed
 - Bug in assessing [`fastnumbers`](https://github.com/SethMMorton/fastnumbers)
   version at import-time ([@hholzgra](https://github.com/hholzgra), issues #51, #53)

[5.2.0] - 2018-02-14
---

### Added
 - `ns.NUMAFTER` to cause numbers to be placed after non-numbers (issues #48, #49)
 - `natcmp` function (Python 2 only) ([@rinslow](https://github.com/rinslow), issue #47)

[5.1.1] - 2017-11-11
---

### Added
 - Additional unicode number support for Python 3.7
 - Information on how to install and test (issue #46)

[5.1.0] - 2017-08-19
---

### Changed
 - All Unicode input is now normalized (issue #44, #45)

### Fixed
 - `StopIteration` warning on Python 3.6+
   ([@lykinsbd](https://github.com/lykinsbd), issues #42, #43)

[5.0.3] - 2017-04-30
---

 - Improved development infrastructure
 - Migrated documentation to ReadTheDocs

[5.0.2] - 2017-01-02
---

### Added
 - Additional unicode number support for Python 3.6
 - "how does it work?" section to the documentation

### Changed
 - Renamed several internal functions and variables to improve clarity
 - Improved documentation examples

[5.0.1] - 2016-06-04
---

### Added
 - The `ns` enum attributes can now be imported from the top-level namespace

### Fixed
 - Bug with the `from natsort import *` mechanism
 - Bug with using `natsort` with `python -OO` (issues #38, #39)

[5.0.0] - 2016-05-08
---

### Added
 - `chain_functions` function for convenience in creating
   a complex user-given `key` from several existing functions

### Changed
 - `ns.LOCALE`/`humansorted` now accounts for thousands separators (issue #36)
 - Refactored entire codebase to be more functional (as in use functions as
   units). Previously, the code was rather monolithic and difficult to follow. The
   goal is that with the code existing in smaller units, contributing will
   be easier (issue #37)
 - Increased speed of execution (came for free with the new functional approach
   because the new factory function paradigm eliminates most `if` branches
   during execution). For the most cases, the code is 30-40% faster than version 4.0.4.
   If using `ns.LOCALE` or `humansorted`, the code is 1100% faster than version 4.0.4
 - Improved clarity of documentaion with regards to locale-aware sorting

### Deprecated
 - `ns.TYPESAFE` option as it is now always on (due to a new
   iterator-based algorithm, the typesafe function is now cheap)

[4.0.4] - 2015-11-01
---

### Changed
 - Improved coverage of unit tests
 - Unit tests use new and improved hypothesis library

### Fixed
 - Compatibility issues with Python 3.5

[4.0.3] - 2015-06-25
---

### Fixed
 - Bad install on last release (sorry guys!) (issue #30)

[4.0.2] - 2015-06-24
---

### Changed
 - Consolidated under-the-hood compatibility functionality

### Fixed
 - Python 2.6 and Python 3.2 compatibility. Unit testing is now
   performed for these versions ([@dpetzold](https://github.com/dpetzold), issue #29)

[4.0.1] - 2015-06-04
---

### Added
 - Support for sorting NaN by internally converting to -Infinity or +Infinity (issue #27)

[4.0.0] - 2015-05-17
---

### Changed
 - Made default behavior of `natsort` search for unsigned ints,
   rather than signed floats. This is a backwards-incompatible
   change but in 99% of use cases it should not require any
   end-user changes (issue #20)
 - Improved handling of locale-aware sorting on systems where the
   underlying locale library is broken (issue #34))
 - Greatly improved all unit tests by adding the `hypothesis` library

[3.5.6] - 2015-04-06
---

### Added
 - `UNGROUPLETTERS` algorithm to get the case-grouping behavior of
   an ordinal sort when using `LOCALE` (issue #23)
 - Convenience functions `decoder`, `as_ascii`, and `as_utf8` for
   dealing with bytes types

[3.5.5] - 2015-04-04
---

### Added
 - `realsorted` and `index_realsorted` functions for forward-compatibility with >= 4.0.0

### Changed
 - Made explanation of when to use `TYPESAFE` more clear in the docs

[3.5.4] - 2015-04-02
---

### Fixed
 - Bug where a `TypeError` was raised if a string containing a leading
   number was sorted with alpha-only strings when `LOCALE` is used (issue #22)

[3.5.3] - 2015-03-26
---

### Changed
 - Documentation updates to better describe locale bug, and illustrate
   upcoming default behavior change
 - Internal improvements, including making test suite more granular

### Fixed
 - Bug where `--reverse-filter` option in shell script was not
   getting checked for correctness

[3.5.2] - 2015-01-13
---

### Added
 - A `pathlib.Path` object is converted to a `str` if `ns.PATH` is enabled (issue #16)

[3.5.1] - 2014-09-25
---

### Changed
 - Refactored modules so that only the public API was in `natsort.py` and `ns_enum.py`
 - Refactored all import statements to be absolute, not relative

### Fixed
 - Bug that caused list/tuples to fail when using `ns.LOWECASEFIRST`
   or `ns.IGNORECASE` (issue #15)

[3.5.0] - 2014-09-02
---

### Added
 - `alg` argument to the `natsort` functions.  This argument
   accepts an enum that is used to indicate the options the user wishes
   to use.  The `number_type`, `signed`, `exp`, `as_path`, and `py3_safe`
   options are being deprecated and will become (undocumented)
   keyword-only options in `natsort` version 4.0.0
 - The `humansorted` convenience function as a convenience to locale-aware sorting
 - The user can now modify how `natsort` handles the case of non-numeric
   characters (issue #14)
 - The user can now instruct `natsort` to use locale-aware sorting, which
   allows `natsort` to perform true "human sorting" (issue #14)
 - Locale functionality to the shell script

[3.4.1] - 2014-08-12
---

### Changed
 - `natsort` will now use the [`fastnumbers`](https://github.com/SethMMorton/fastnumbers)
   module if it is installed. This gives up to an extra 30% boost in speed over
   the previous performance enhancements
 - Made documentation point to more `natsort` resources, and also added a
   new example in the examples section

[3.4.0] - 2014-07-19
---

### Added
 - `natsort_keygen` function that will generate a wrapped version
   of `natsort_key` that is easier to call.  `natsort_key` is now set to
   deprecate at natsort version 4.0.0
 - `as_path` option to `natsorted` & co. that will try to treat
   input strings as filepaths. This will help yield correct results for
   OS-generated inputs like
   `['/p/q/o.x', '/p/q (1)/o.x', '/p/q (10)/o.x', '/p/q/o (1).x']` (issue #3)
 - `order_by_index` function to help in using the output of
   `index_natsorted` and `index_versorted`
 - `reverse` option to `natsorted` & co. to make it's API more
   similar to the builtin 'sorted'
 - More unit tests
 - Auxillary test code that helps in profiling and stress-testing
 - Support for coveralls.io

### Changed
 - Massive performance enhancements for string input (1.8x-2.0x), at the expense
   of reduction in speed for numeric input (~2.0x) - note that sorting numbers\
   still only takes 0.6x the time of sorting strings
 - Entire codebase is now PyFlakes and PEP8 compliant
 - Reworked the documentation, moving most of it to PyPI's hosting platform

### Fixed
 - Bug that caused user's options to the `natsort_key` to not be
   passed on to recursive calls of `natsort_key` (issue #12)

[3.3.0] - 2014-06-28
---

### Added
 - `versorted` method for more convenient sorting of versions (issue #11)
 - Unit test coverage (99%)

### Changed
 - Updated command-line tool `--number_type` option with 'version' and 'ver'
   to make it more clear how to sort version numbers
 - Moved unit-testing mechanism from being docstring-based to actual unit tests
   in actual functions (issue #10)
 - Made docstrings for public functions mirror the README API
 - Connected `natsort` development to Travis-CI to help ensure quality releases

[3.2.1] - 2014-06-20
---

### Fixed
 - Re-"Fixed" unorderable types issue on Python 3.x - this workaround
   is for when the problem occurs in the middle of the string (issue #7 again)

[3.2.0] - 2014-05-07
---

### Fixed
 - "Fixed" unorderable types issue on Python 3.x with a workaround that
   attempts to replicate the Python 2.x behavior by putting all the numbers
   (or strings that begin with numbers) first (issue #7)

### Removed
 - Now explicitly excluding `__pycache__` from releases by adding a prune statement
   to MANIFEST.in

[3.1.2] - 2014-05-05
---

### Added
 - `setup.cfg` to support universal wheels (issue #6)
 - Python 3.0 and Python 3.1 as requiring the argparse module

[3.1.1] - 2014-03-01
---

### Added
 - Ability to sort lists of lists (issue #5)

### Changed
 - Cleaned up import statements

[3.1.0] - 2014-01-20
---

### Added
 - `signed` and `exp` options to allow finer tuning of the sorting
 - Doctests
 - New shell script options that correspond to `signed` and `exp`
 - In the shell script the user can now specify multiple numbers to exclude or multiple ranges

### Changed
 - Entire codebase now works for both Python 2 and Python 3 without needing to run `2to3`
 - Updated all doctests
 - Further simplified the `natsort` base code by removing unneeded functions.
 - Simplified documentation where possible
 - Improved the shell script code
 - Made the shell script documentation less "path"-centric to make it clear it is not
   just for sorting file paths

### Removed
 - The shell script filesystem-based options because these can be achieved better though
a pipeline by which to filter

[3.0.2] - 2013-10-01
---

### Changed
 - Made float, int, and digit searching algorithms all share the same base function
 - Made the `__version__` variable available when importing the module

### Fixed
 - Outdated comments

[3.0.1] - 2013-08-15
---

### Added
 - Support for unicode strings (issue #2)

### Fixed
 - Empty string removal function

### Removed
 - Extraneous `string2int` function

[3.0.0] - 2013-07-13
---

### Added
 - A `number_type` argument to the sorting functions to specify how liberal to be when
   deciding what a number is

### Changed
 - Reworked the documentation

[2.2.0] - 2013-06-25
---

### Added
 - `key` attribute to `natsorted` and `index_natsorted` so that it mimics the functionality
   of the built-in `sorted` (issue #1)
 - Tests to reflect the new functionality, as well as tests demonstrating how to get similar
   functionality using `natsort_key`

[2.1.0] - 2012-12-05
---

### Changed
 - Reorganized package
 - Now using a platform independent shell script generator (`entry_points` from distribute)
 - Can now execute `natsort` from command line with `python -m natsort` as well

[2.0.2] - 2012-11-30
---

### Added
 - The `use_2to3` option to `setup.py`
 - Include `distribute_setup.py` to the distribution
 - Dependency to the `argparse` module (for python2.6)

[2.0.1] - 2012-11-21
---

### Added
 - Tests into the natsort.py file iteself

### Changed
 - Reorganized directory structure

[2.0.0] - 2012-11-16
---

### Added
 - Better README documentation
 - Doctests

### Changed
 - Sorting algorithm to support floats (including exponentials) and basic version number support

<!---Comparison links-->
[7.1.1]: https://github.com/SethMMorton/natsort/compare/7.1.0...7.1.1
[7.1.0]: https://github.com/SethMMorton/natsort/compare/7.0.1...7.1.0
[7.0.1]: https://github.com/SethMMorton/natsort/compare/7.0.0...7.0.1
[7.0.0]: https://github.com/SethMMorton/natsort/compare/6.2.0...7.0.0
[6.2.0]: https://github.com/SethMMorton/natsort/compare/6.1.0...6.2.0
[6.1.0]: https://github.com/SethMMorton/natsort/compare/6.0.0...6.1.0
[6.0.0]: https://github.com/SethMMorton/natsort/compare/5.5.0...6.0.0
[5.5.0]: https://github.com/SethMMorton/natsort/compare/5.4.1...5.5.0
[5.4.1]: https://github.com/SethMMorton/natsort/compare/5.4.0...5.4.1
[5.4.0]: https://github.com/SethMMorton/natsort/compare/5.3.3...5.4.0
[5.3.3]: https://github.com/SethMMorton/natsort/compare/5.3.2...5.3.3
[5.3.2]: https://github.com/SethMMorton/natsort/compare/5.3.1...5.3.2
[5.3.1]: https://github.com/SethMMorton/natsort/compare/5.3.0...5.3.1
[5.3.0]: https://github.com/SethMMorton/natsort/compare/5.2.0...5.3.0
[5.2.0]: https://github.com/SethMMorton/natsort/compare/5.1.1...5.2.0
[5.1.1]: https://github.com/SethMMorton/natsort/compare/5.1.0...5.1.1
[5.1.0]: https://github.com/SethMMorton/natsort/compare/5.0.3...5.1.0
[5.0.3]: https://github.com/SethMMorton/natsort/compare/5.0.2...5.0.3
[5.0.2]: https://github.com/SethMMorton/natsort/compare/5.0.1...5.0.2
[5.0.1]: https://github.com/SethMMorton/natsort/compare/5.0.0...5.0.1
[5.0.0]: https://github.com/SethMMorton/natsort/compare/4.0.4...5.0.0
[4.0.4]: https://github.com/SethMMorton/natsort/compare/4.0.3...4.0.4
[4.0.3]: https://github.com/SethMMorton/natsort/compare/4.0.2...4.0.3
[4.0.2]: https://github.com/SethMMorton/natsort/compare/4.0.1...4.0.2
[4.0.1]: https://github.com/SethMMorton/natsort/compare/4.0.0...4.0.1
[4.0.0]: https://github.com/SethMMorton/natsort/compare/3.5.6...4.0.0
[3.5.6]: https://github.com/SethMMorton/natsort/compare/3.5.5...3.5.6
[3.5.5]: https://github.com/SethMMorton/natsort/compare/3.5.4...3.5.5
[3.5.4]: https://github.com/SethMMorton/natsort/compare/3.5.3...3.5.4
[3.5.3]: https://github.com/SethMMorton/natsort/compare/3.5.2...3.5.3
[3.5.2]: https://github.com/SethMMorton/natsort/compare/3.5.1...3.5.2
[3.5.1]: https://github.com/SethMMorton/natsort/compare/3.5.0...3.5.1
[3.5.0]: https://github.com/SethMMorton/natsort/compare/3.4.1...3.5.0
[3.4.1]: https://github.com/SethMMorton/natsort/compare/3.4.0...3.4.1
[3.4.0]: https://github.com/SethMMorton/natsort/compare/3.3.0...3.4.0
[3.3.0]: https://github.com/SethMMorton/natsort/compare/3.2.1...3.3.0
[3.2.1]: https://github.com/SethMMorton/natsort/compare/3.2.0...3.2.1
[3.2.0]: https://github.com/SethMMorton/natsort/compare/3.1.2...3.2.0
[3.1.2]: https://github.com/SethMMorton/natsort/compare/3.1.1...3.1.2
[3.1.1]: https://github.com/SethMMorton/natsort/compare/3.1.0...3.1.1
[3.1.0]: https://github.com/SethMMorton/natsort/compare/3.0.2...3.1.0
[3.0.2]: https://github.com/SethMMorton/natsort/compare/3.0.1...3.0.2
[3.0.1]: https://github.com/SethMMorton/natsort/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/SethMMorton/natsort/compare/2.2.0...3.0.0
[2.2.0]: https://github.com/SethMMorton/natsort/compare/2.1.0...2.2.0
[2.1.0]: https://github.com/SethMMorton/natsort/compare/2.0.2...2.1.0
[2.0.2]: https://github.com/SethMMorton/natsort/compare/2.0.1...2.0.2
[2.0.1]: https://github.com/SethMMorton/natsort/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/SethMMorton/natsort/releases/tag/2.0.0
