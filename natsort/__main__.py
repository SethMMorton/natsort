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
    parser.add_argument('-e', '--exclude', help='Used to exclude an entry '
                        'that contains a specific number.')
    parser.add_argument('-r', '--reverse', help='Returns in reversed order.',
                        action='store_true', default=False)
    parser.add_argument('-t', '--number_type', choices=('digit', 'int', 'float'),
                         default='float', help='Choose the type of number '
                         'to search for.')
    parser.add_argument('entries', help='The entries to sort. Taken from stdin '
                        'if nothing is given on the command line.', nargs='*',
                        default=sys.stdin)
    args = parser.parse_args()

    # Make sure the filter range is given properly. Does nothing if no filter
    filterdata = check_filter(args.filter)

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
    sort_and_print_entries(entries, filterdata, args.exclude, args.reverse, args.number_type)

def range_check(low, high):
    """\
    Verifies that that given range has a low lower than the high.
    """
    low, high = float(low), float(high)
    if low >= high:
        raise ValueError('low >= high')
    else:
        return low, high

def check_filter(filt):
    """Check that the low value of the filter is lower than the high."""
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


def keep_entry(entry, low, high, converter, regex):
    """Boolean function to determine if an entry should be kept out"""
    return any(low <= converter(num) <= high for num in regex.findall(entry))


def sort_and_print_entries(entries, filterdata, exclude, reverse, number_type):
    """Sort the entries, applying the filters first if necessary.
    """

    number_type = {'digit': None, 'int': int, 'float': float}[number_type]
    inp_options = (number_type, True, True)
    regex, num_function = regex_and_num_function_chooser[inp_options]

    # Pre-remove entries that don't pass the filtering criteria
    if filterdata is not None:
        low, high = filterdata
        entries = [entry for entry in entries if keep_entry(entry, low, high, num_function, regex)]
    if exclude:
        entries = [entry for entry in entries if exclude not in entry]

    # Print off the sorted results
    key = lambda x: natsort_key(x, number_type=number_type, signed=True, exp=True)
    entries.sort(key=key, reverse=reverse)
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

if __name__ == '__main__':
    try:
        main()
    except ValueError as a:
        sys.exit(py23_str(a))
    except KeyboardInterrupt:
        sys.exit(1)
