# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
import sys
import os
import re
from .natsort import natsort_key, natsorted, int_nosign_re, int_sign_re
from .natsort import float_sign_exp_re, float_nosign_exp_re
from .natsort import float_sign_noexp_re, float_nosign_noexp_re
from .natsort import regex_and_num_function_chooser
from ._version import __version__
from .py23compat import py23_str


def main():
    """\
    Performs a natural sort on entries given on the command-line.
    A natural sort sorts numerically then alphabetically, and will sort
    by numbers in the middle of a pathname.
    """

    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    from textwrap import dedent
    parser = ArgumentParser(description=dedent(main.__doc__),
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(__version__))
    parser.add_argument('-f', '--filter', help='Used for '
                        'keeping only the entries that have a number '
                        'falling in the given range.', nargs=2, type=float,
                        metavar=('LOW', 'HIGH'))
    parser.add_argument('-e', '--exclude', type=float, help='Used to exclude an entry '
                        'that contains a specific number.')
    parser.add_argument('-r', '--reverse', help='Returns in reversed order.',
                        action='store_true', default=False)
    parser.add_argument('-t', '--number_type', choices=('digit', 'int', 'float'),
                         default='float', help='Choose the type of number '
                         'to search for.')
    parser.add_argument('--test', default=False, action='store_true',
                        help='Execute doctests on this file. '
                             'No other actions will be performed.')
    parser.add_argument('entries', help='The entries to sort. Taken from stdin '
                        'if nothing is given on the command line.', nargs='*',
                        default=sys.stdin)
    args = parser.parse_args()

    # Run tests if requested
    if args.test:
        raise ExecuteTestRunner

    # Make sure the filter range is given properly. Does nothing if no filter
    args.filter = check_filter(args.filter)

    # # Recursively collect entries, if necessary.
    # if args.recursive:
    #     jn = os.path.join
    #     entries = [jn(p, fn) for p, d, f in os.walk(os.curdir) for fn in f]
    # # Collect entries either from a pipe or the command-line arguments.
    # else:
    #     entries = [f.strip() for f in args.entries]
    # Remove trailing whitespace from all the entries
    entries = [e.strip() for e in args.entries]

    # # Split into directory path and filenames
    # entries = split_entries(entries, args.onlyfiles)

    # Sort by directory then by file within directory and print.
    sort_and_print_entries(entries, args)

def range_check(low, high):
    """\
    Verifies that that given range has a low lower than the high.

        >>> range_check(10, 11)
        (10.0, 11.0)
        >>> range_check(6.4, 30)
        (6.4, 30.0)
        >>> try:
        ...    range_check(7, 2)
        ... except ValueError as e:
        ...    print(e)
        low >= high

    """
    low, high = float(low), float(high)
    if low >= high:
        raise ValueError('low >= high')
    else:
        return low, high

def check_filter(filt):
    """\
    Check that the low value of the filter is lower than the high.
    If there is to be no filter, return 'None'.

        >>> check_filter(())
        >>> check_filter(False)
        >>> check_filter(None)
        >>> check_filter((6, 7))
        (6.0, 7.0)
        >>> try:
        ...    check_filter((7, 2))
        ... except ValueError as e:
        ...    print(e)
        Error in --filter: low >= high

    """
    # Quick return if no filter.
    if not filt:
        return None
    try:
        return range_check(filt[0], filt[1])
    except ValueError as a:
        raise ValueError('Error in --filter: '+py23_str(a))

# def split_entries(entries, a):
#     """For each file, separate into directory and filename. Store all files
#     in a dir into a dict where the dir is the key and filename is the value.
#     """
#     dirs = {}
#     for path in entries:
#         if a:
#             try:
#                 with open(path) as fl:
#                     pass
#             except IOError:
#                 continue
#         dir, file = os.path.split(path)
#         try:
#             dirs[dir].append(file)
#         except KeyError:
#             dirs[dir] = []
#             dirs[dir].append(file)
#     return dirs


def keep_entry_range(entry, low, high, converter, regex):
    """\
    Boolean function to determine if an entry should be kept out
    based on if any numbers are in a given range.

        >>> import re
        >>> regex = re.compile(r'\d+')
        >>> keep_entry_range('a56b23c89', 0, 100, int, regex)
        True
        >>> keep_entry_range('a56b23c89', 88, 90, int, regex)
        True
        >>> keep_entry_range('a56b23c89', 1, 20, int, regex)
        False

    """
    return any(low <= converter(num) <= high for num in regex.findall(entry))


def exclude_entry(entry, val, converter, regex):
    """\
    Boolean function to determine if an entry should be kept out
    based on if it contains a specific number.

        >>> import re
        >>> regex = re.compile(r'\d+')
        >>> exclude_entry('a56b23c89', 100, int, regex)
        True
        >>> exclude_entry('a56b23c89', 23, int, regex)
        False

    """
    return not any(converter(num) == val for num in regex.findall(entry))


def sort_and_print_entries(entries, args):
    """\
    Sort the entries, applying the filters first if necessary.
    
        >>> class Args:
        ...     def __init__(self, filter, exclude, reverse, number_type):
        ...         self.filter = filter
        ...         self.exclude = exclude
        ...         self.reverse = reverse
        ...         self.number_type = number_type
        >>> entries = ['tmp/a57/path2',
        ...            'tmp/a23/path1',
        ...            'tmp/a1/path1', 
        ...            'tmp/a130/path1',
        ...            'tmp/a64/path1',
        ...            'tmp/a64/path2']
        >>> sort_and_print_entries(entries, Args(None, False, False, 'float'))
        tmp/a1/path1
        tmp/a23/path1
        tmp/a57/path2
        tmp/a64/path1
        tmp/a64/path2
        tmp/a130/path1
        >>> sort_and_print_entries(entries, Args((20, 100), False, False, 'float'))
        tmp/a23/path1
        tmp/a57/path2
        tmp/a64/path1
        tmp/a64/path2
        >>> sort_and_print_entries(entries, Args(None, 23, False, 'float'))
        tmp/a1/path1
        tmp/a57/path2
        tmp/a64/path1
        tmp/a64/path2
        tmp/a130/path1
        >>> sort_and_print_entries(entries, Args(None, 2, False, 'float'))
        tmp/a1/path1
        tmp/a23/path1
        tmp/a64/path1
        tmp/a130/path1
        >>> sort_and_print_entries(entries, Args(None, False, True, 'float'))
        tmp/a130/path1
        tmp/a64/path2
        tmp/a64/path1
        tmp/a57/path2
        tmp/a23/path1
        tmp/a1/path1

    """

    number_type = {'digit': None, 'int': int, 'float': float}[args.number_type]
    inp_options = (number_type, True, True)
    regex, num_function = regex_and_num_function_chooser[inp_options]

    # Pre-remove entries that don't pass the filtering criteria
    if args.filter is not None:
        low, high = args.filter
        entries = [entry for entry in entries
                        if keep_entry_range(entry, low, high, num_function, regex)]
    if args.exclude:
        exclude = args.exclude
        entries = [entry for entry in entries
                        if exclude_entry(entry, exclude, num_function, regex)]

    # Print off the sorted results
    key = lambda x: natsort_key(x, number_type=number_type, signed=True, exp=True)
    entries.sort(key=key, reverse=args.reverse)
    for entry in entries:
        print(entry)
    # for dir in natsorted(entries, number_type=number_type):
    #     entries[dir].sort(key=lambda x: natsort_key(x, number_type=number_type),
    #                    reverse=reverse)
    #     for file in entries[dir]:
    #         if filterdata is not None:
    #             # Find all the numbers in the filename.
    #             nums = filterdata[2].findall(file)
    #             # If any numbers are between the range, print.
    #             # Otherwise, move to next file.
    #             for num in nums:
    #                 if filterdata[0] <= float(num) <= filterdata[1]: break
    #             else:
    #                 continue
    #         if exclude and exclude in file: continue
    #         print(os.path.join(dir, file))


class ExecuteTestRunner(Exception):
    """Class used to quit execution and run the doctests"""
    pass


if __name__ == '__main__':
    try:
        main()
    except ValueError as a:
        sys.exit(py23_str(a))
    except KeyboardInterrupt:
        sys.exit(1)
    except ExecuteTestRunner:
        import doctest
        ret = doctest.testmod()
        if ret[0] == 0:
            print('natsort: All {0[1]} tests successful!'.format(ret))
