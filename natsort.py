#! /usr/bin/env python

from __future__ import print_function, division
import sys
import os
import re
num_splitter = re.compile(r'(\d+|\D+)')

def main():
    '''\
    Performs a natural sort on pathnames given on the command-line.
    A natural sort sorts numerically then alphabetically, and will sort
    by numbers in the middle of a pathname.
    '''

    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    from textwrap import dedent
    parser = ArgumentParser(description=dedent(main.__doc__),
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='version', version='%(prog)s 1.2')
    parser.add_argument('-a', '--all', help='By default, only real files that '
                        'are readable and non-empty are listed.  This will '
                        'also list folders and undeadable files.',
                        action='store_true', default=False)
    parser.add_argument('-f', '--filter', help='Used for '
                        'filtering out only the files that have a number '
                        'falling in the given range.', nargs=2, type=float,
                        metavar=('LOW', 'HIGH'))
    parser.add_argument('-e', '--exclude', help='Used to exclude a specific '
                        'number.')
    parser.add_argument('-r', '--reverse', help='Returns in reversed order.',
                        action='store_true', default=False)
    parser.add_argument('-R', '--recursive', help='Recursively decend the '
                        'directory tree.', action='store_true', default=False)
    parser.add_argument('paths', help='The paths to sort.', nargs='*',
                        default=sys.stdin)
    args = parser.parse_args()

    # Make sure the filter range is given properly. Does nothing if no filter
    filterdata = check_filter(args.filter)

    # Recursively collect paths, if necessary.
    if args.recursive:
        jn = os.path.join
        paths = [jn(p, fn) for p, d, f in os.walk(os.curdir) for fn in f]
    # Collect paths either from a pipe or the command-line arguments.
    else:
        paths = [f.strip() for f in args.paths]

    # Split into directory path and filenames
    paths = split_paths(paths, args.all)

    # Sort by directory then by file within directory and print.
    sort_and_print_paths(paths, filterdata, args.exclude, args.reverse)


#################################
# ACTUAL SORTING KEYS/SUBROUTINES
#################################

def natsort_key(s):
    '''\
    Key to sort strings and numbers naturally, not by ASCII.
    For use in passing to the :py:func:`sorted` builtin or
    :py:meth:`sort` attribute of lists.
    '''
    # Split
    try:
        s = num_splitter.findall(s)
    except TypeError:
        s = [s]
    # Convert floats that were split on the decimal back into floats
    ix = next((i for i, x in enumerate(s) if x == '.'), False)
    while ix:
        # Dots at front or back of the string don't affect sorting
        if ix == 0 or ix == len(s)-1:
            pass
        # If the elements in the front and back of a dot are ints,
        # then it is considered the decimal point in a float.
        # Construct this float
        elif s[ix-1].isdigit() and s[ix+1].isdigit():
            flt = float(s[ix-1]+'.'+s[ix+1])
            # Check if the float is negative or not.
            if s[ix-2].endswith('-'):
                s[ix-2] = s[ix-2][0:len(s)-1] # Remove dash from string.
                flt = -flt
            # Replace the three string that made up the float with the float
            s = s[0:ix-1] + [flt] + s[ix+2:]
        ix = next((i for i, x in enumerate(s) if x == '.'), False)
    # Now, convert remaining ints to int and return.
    return [string2int(x) for x in s]

def natsorted(seq):
    '''\
    Sorts a sequence naturally (alphabetically and numerically),
    not by ASCII.

    :argument seq:
        The sequence to be sorted.
    :type seq: sequence-like
    :rtype: list
    '''
    return sorted(seq, key=natsort_key)

def index_natsorted(seq):
    '''\
    Sorts a sequence naturally, but returns a list of sorted the 
    indeces and not the sorted list.

    :argument seq:
        The sequence that you want the sorted index of.
    :type seq: sequence-like
    :rtype: list
    '''
    # Pair the index and sequence together, then sort by 
    index_seq_pair = [[x, y] for x, y in zip(range(len(seq)), seq)]
    index_seq_pair.sort(key=lambda x: natsort_key(x[1]))
    return [x[0] for x in index_seq_pair]


######################
# Included Subroutines
######################

def string2int(string):
    '''Convert to integer if an integer string.'''
    try:
        if string.isdigit():
            return int(string)
        else:
            return string
    except:
        return string

def range_check(low, high):
    '''\
    Verifies that that given range has a low lower than the high.
    '''
    low, high = float(low), float(high)
    if low >= high:
        raise ValuError('low >= high')
    else:
        return low, high

def check_filter(filt):
    '''Check that the low value of the filter is lower than the high.'''
    # Quick return if no filter.
    if not filt:
        return None
    try:
        low, high = range_check(filt[0], filt[1])
    except AssertionError as a:
        raise AssertionError ('Error in --filter: '+str(a))
    return low, high, re.compile(r'[+-]?\d+\.?\d*')

def split_paths(paths, a):
    '''For each file, separate into directory and filename. Store all files
    in a dir into a dict where the dir is the key and filename is the value.
    '''
    dirs = {}
    for path in paths:
        if not a:
            try:
                with open(path) as fl:
                    pass
            except IOError:
                continue
        dir, file = os.path.split(path)
        try:
            dirs[dir].append(file)
        except KeyError:
            dirs[dir] = []
            dirs[dir].append(file)
    return dirs

def sort_and_print_paths(dirs, filterdata, exclude, reverse):
    '''Sort the paths by directoy then by file within that directory.
    Print off the results.
    '''
    for dir in natsorted(dirs.keys()):
        dirs[dir].sort(key=natsort_key)
        if reverse:
            dirs[dir] = reversed(dirs[dir])
        for file in dirs[dir]:
            if filterdata is not None:
                # Find all the numbers in the filename.
                nums = filterdata[2].findall(file)
                # If any numbers are between the range, print.
                # Otherwise, move to next file.
                for num in nums:
                    if filterdata[0] <= float(num) <= filterdata[1]: break
                else:
                    continue
            if exclude and exclude in file: continue
            print(os.path.join(dir, file))

if __name__ == '__main__':
    try:
        main()
    except AssertionError as a:
        sys.exit(str(a))
    except KeyboardInterrupt:
        sys.exit(1)
