#! /usr/bin/env python
__version__ = '1.2.0'

import re
splitter = re.compile(r'(\d+|\D+)')

__all__ = [
           'natsort_key',
           'natsorted',
           'index_natsorted',
          ]

def string2int(string):
    '''Convert to integer if an integer string.'''
    if not isinstance(string, str):
        return string
    try:
        return int(string)
    except ValueError:
        return string

def natsort_key(s):
    '''\
    Key to sort strings and numbers naturally, not by ASCII.
    For use in passing to the :py:func:`sorted` builtin or
    :py:meth:`sort` attribute of lists.
    '''
    # Split.  If not possible, just return 
    try:
        s = splitter.findall(s)
    except TypeError:
        return (s,)

    # Loop over each element of the split string and try to parse
    # numbers into tuples.  I.E 4.5 => (4, 5) or 4.5.3.2 => (4, 5, 3, 2)
    maxind = len(s)
    ix = 0
    t = []
    while ix < maxind:

        # If this element corresponds to a non-number, do nothing more
        if not s[ix].isdigit():
            t.append(s[ix])
            ix += 1
            continue

        # Otherwise try to build up a numbers tuple
        tmp = [int(s[ix])]

        # If there is a dot and number after this number, add it
        while True:

            # Make sure that there is a . and number up next, also
            # ensuring that we aren't checking elemnts that don't exist
            try:
                if not (s[ix+1] == '.' and s[ix+2].isdigit()):
                    ix += 1
                    break
            except IndexError:
                ix += 1
                break

            # Add the next number to the tuple
            ix += 2
            tmp.append(int(s[ix]))

        # If there are only two elements, assume that this is a float
        if len(tmp) == 2:
            tmp = [float('.'.join([str(tmp[0]), str(tmp[1])]))]

        # Last, if this is a float or just an int (length 1) and the
        # previous element ends with a dash, assume this is a negative
        # sign
        if len(tmp) == 1:
            try:
                if t[-1].endswith('-'):
                    tmp[0] = -tmp[0]
                    t[-1] = t[-1][0:-2]
            except AttributeError:
                pass

        # Add this to the list to return
        t.append(tmp)

    # Now, convert this list to a tuple
    return tuple(t)

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
    index_seq_pair = [[x, y] for x, y in zip(xrange(len(seq)), seq)]
    index_seq_pair.sort(key=lambda x: natsort_key(x[1]))
    return [x[0] for x in index_seq_pair]
