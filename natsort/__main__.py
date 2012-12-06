from __future__ import print_function, division
import sys
import os
import re
from natsort import natsort_key, natsorted
from _version import __version__

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
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(__version__))
    parser.add_argument('-F', '--onlyfiles', help='Only files that '
                        'are readable and non-empty are read in.  '
                        'This will exculude folders from being read in.',
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
    paths = split_paths(paths, args.onlyfiles)

    # Sort by directory then by file within directory and print.
    sort_and_print_paths(paths, filterdata, args.exclude, args.reverse)

def range_check(low, high):
    '''\
    Verifies that that given range has a low lower than the high.
    '''
    low, high = float(low), float(high)
    if low >= high:
        raise ValueError ('low >= high')
    else:
        return low, high

def check_filter(filt):
    '''Check that the low value of the filter is lower than the high.'''
    # Quick return if no filter.
    if not filt:
        return None
    try:
        low, high = range_check(filt[0], filt[1])
    except ValueError as a:
        raise ValueError ('Error in --filter: '+str(a))
    return low, high, re.compile(r'[+-]?\d+\.?\d*')

def split_paths(paths, a):
    '''For each file, separate into directory and filename. Store all files
    in a dir into a dict where the dir is the key and filename is the value.
    '''
    dirs = {}
    for path in paths:
        if a:
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
    except ValueError as a:
        sys.exit(str(a))
    except KeyboardInterrupt:
        sys.exit(1)
