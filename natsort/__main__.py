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
    by numbers in the middle of an entry.

        >>> import sys
        >>> sys.argv[1:] = ['num-2', 'num-6', 'num-1']
        >>> main()
        num-6
        num-2
        num-1
        >>> sys.argv[1:] = ['-r', 'num-2', 'num-6', 'num-1']
        >>> main()
        num-1
        num-2
        num-6
        >>> sys.argv[1:] = ['--nosign', 'num-2', 'num-6', 'num-1']
        >>> main()
        num-1
        num-2
        num-6
        >>> sys.argv[1:] = ['-t', 'digit', 'num-2', 'num-6', 'num-1']
        >>> main()
        num-1
        num-2
        num-6
        >>> sys.argv[1:] = ['-t', 'int', '-e', '-1', '-e', '6',
        ...                 'num-2', 'num-6', 'num-1']
        >>> main()
        num-6
        num-2
        >>> sys.argv[1:] = ['-t', 'digit', '-e', '1', '-e', '6',
        ...                 'num-2', 'num-6', 'num-1']
        >>> main()
        num-2
        >>> sys.argv[1:] = ['a1.0e3', 'a5.3', 'a453.6']
        >>> main()
        a5.3
        a453.6
        a1.0e3
        >>> sys.argv[1:] = ['-f', '1', '10', 'a1.0e3', 'a5.3', 'a453.6']
        >>> main()
        a5.3
        >>> sys.argv[1:] = ['-f', '1', '10', '-f', '400', '500', 'a1.0e3', 'a5.3', 'a453.6']
        >>> main()
        a5.3
        a453.6
        >>> sys.argv[1:] = ['--noexp', 'a1.0e3', 'a5.3', 'a453.6']
        >>> main()
        a1.0e3
        a5.3
        a453.6

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
                        metavar=('LOW', 'HIGH'), action='append')
    parser.add_argument('-e', '--exclude', type=float, action='append',
                        help='Used to exclude an entry '
                        'that contains a specific number.')
    parser.add_argument('-r', '--reverse', help='Returns in reversed order.',
                        action='store_true', default=False)
    parser.add_argument('-t', '--number_type', choices=('digit', 'int', 'float'),
                         default='float', help='Choose the type of number '
                         'to search for. "float" will search for floating-point '
                         'numbers.  "int" will only search for integers. '
                         '"digit" is a shortcut for "int" with --nosign.')
    parser.add_argument('--nosign', default=True, action='store_false',
                        dest='signed', help='Do not consider "+" or "-" as part '
                        'of a number, i.e. do not take sign into consideration.')
    parser.add_argument('--noexp', default=True, action='store_false',
                        dest='exp', help='Do not consider an exponential as part '
                        'of a number, i.e. 1e4, would be considered as 1, "e", '
                        'and 4, not as 10000.  This only effects the '
                        '--number_type=float.')
    parser.add_argument('entries', help='The entries to sort. Taken from stdin '
                        'if nothing is given on the command line.', nargs='*',
                        default=sys.stdin)
    args = parser.parse_args()

    # Make sure the filter range is given properly. Does nothing if no filter
    args.filter = check_filter(args.filter)

    # Remove trailing whitespace from all the entries
    entries = [e.strip() for e in args.entries]

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
        >>> check_filter([(6, 7)])
        [(6.0, 7.0)]
        >>> check_filter([(6, 7), (2, 8)])
        [(6.0, 7.0), (2.0, 8.0)]
        >>> try:
        ...    check_filter([(7, 2)])
        ... except ValueError as e:
        ...    print(e)
        Error in --filter: low >= high

    """
    # Quick return if no filter.
    if not filt:
        return None
    try:
        return [range_check(f[0], f[1]) for f in filt]
    except ValueError as a:
        raise ValueError('Error in --filter: '+py23_str(a))


def keep_entry_range(entry, lows, highs, converter, regex):
    """\
    Boolean function to determine if an entry should be kept out
    based on if any numbers are in a given range.

        >>> import re
        >>> regex = re.compile(r'\d+')
        >>> keep_entry_range('a56b23c89', [0], [100], int, regex)
        True
        >>> keep_entry_range('a56b23c89', [1, 88], [20, 90], int, regex)
        True
        >>> keep_entry_range('a56b23c89', [1], [20], int, regex)
        False

    """
    return any(low <= converter(num) <= high
                  for num in regex.findall(entry)
                  for low, high in zip(lows, highs))


def exclude_entry(entry, values, converter, regex):
    """\
    Boolean function to determine if an entry should be kept out
    based on if it contains a specific number.

        >>> import re
        >>> regex = re.compile(r'\d+')
        >>> exclude_entry('a56b23c89', [100], int, regex)
        True
        >>> exclude_entry('a56b23c89', [23], int, regex)
        False

    """
    return not any(converter(num) in values for num in regex.findall(entry))


def sort_and_print_entries(entries, args):
    """\
    Sort the entries, applying the filters first if necessary.
    
        >>> class Args:
        ...     def __init__(self, filter, exclude, reverse):
        ...         self.filter = filter
        ...         self.exclude = exclude
        ...         self.reverse = reverse
        ...         self.number_type = 'float'
        ...         self.signed = True
        ...         self.exp = True
        >>> entries = ['tmp/a57/path2',
        ...            'tmp/a23/path1',
        ...            'tmp/a1/path1', 
        ...            'tmp/a130/path1',
        ...            'tmp/a64/path1',
        ...            'tmp/a64/path2']
        >>> sort_and_print_entries(entries, Args(None, False, False))
        tmp/a1/path1
        tmp/a23/path1
        tmp/a57/path2
        tmp/a64/path1
        tmp/a64/path2
        tmp/a130/path1
        >>> sort_and_print_entries(entries, Args([(20, 100)], False, False))
        tmp/a23/path1
        tmp/a57/path2
        tmp/a64/path1
        tmp/a64/path2
        >>> sort_and_print_entries(entries, Args(None, [23, 130], False))
        tmp/a1/path1
        tmp/a57/path2
        tmp/a64/path1
        tmp/a64/path2
        >>> sort_and_print_entries(entries, Args(None, [2], False))
        tmp/a1/path1
        tmp/a23/path1
        tmp/a64/path1
        tmp/a130/path1
        >>> sort_and_print_entries(entries, Args(None, False, True))
        tmp/a130/path1
        tmp/a64/path2
        tmp/a64/path1
        tmp/a57/path2
        tmp/a23/path1
        tmp/a1/path1

    """

    # Extract the proper number type.
    kwargs = {'number_type': {'digit': None, 'int': int, 'float': float}[args.number_type],
              'signed': args.signed,
              'exp': args.exp}

    # Pre-remove entries that don't pass the filtering criteria
    # Make sure we use the same searching algorithm for filtering as for sorting.
    if args.filter is not None or args.exclude:
        inp_options = (kwargs['number_type'], args.signed, args.exp)
        regex, num_function = regex_and_num_function_chooser[inp_options]
        if args.filter is not None:
            lows, highs = [f[0] for f in args.filter], [f[1] for f in args.filter]
            entries = [entry for entry in entries
                            if keep_entry_range(entry, lows, highs, num_function, regex)]
        if args.exclude:
            exclude = set(args.exclude)
            entries = [entry for entry in entries
                            if exclude_entry(entry, exclude, num_function, regex)]

    # Print off the sorted results
    entries.sort(key=lambda x: natsort_key(x, **kwargs), reverse=args.reverse)
    for entry in entries:
        print(entry)


if __name__ == '__main__':
    try:
        main()
    except ValueError as a:
        sys.exit(py23_str(a))
    except KeyboardInterrupt:
        sys.exit(1)
    # import doctest
    # ret = doctest.testmod()
    # if ret[0] == 0:
    #     print('natsort: All {0[1]} tests successful!'.format(ret))
