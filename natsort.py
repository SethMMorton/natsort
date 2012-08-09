#! /usr/bin/env python
__version__ = '1.2.0'

import re
num_splitter = re.compile(r'(\d+|\D+)')

__all__ = [
           'natsort_key',
           'natsorted',
           'index_natsorted',
          ]

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
