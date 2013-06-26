'''
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.

    >>> a = ['a2', 'a8', 'a7', 'a5', 'a9', 'a1', 'a4', 'a10', 'a3', 'a6']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']
    >>> natsorted(a)
    ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10']

    >>> a = ['a50', 'a51.', 'a50.4', 'a5.034e1', 'a50.300']
    >>> sorted(a)
    ['a5.034e1', 'a50', 'a50.300', 'a50.4', 'a51.']
    >>> natsorted(a)
    ['a50', 'a50.300', 'a5.034e1', 'a50.4', 'a51.']

    >>> a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    >>> sorted(a)
    ['1.10.1', '1.11', '1.11.4', '1.9.9a', '1.9.9b']
    >>> natsorted(a)
    ['1.9.9a', '1.9.9b', '1.10.1', '1.11.4', '1.11']
    >>> a = ['1.9.9a', '1.11.0', '1.9.9b', '1.11.4', '1.10.1']
    >>> natsorted(a)
    ['1.9.9a', '1.9.9b', '1.10.1', '1.11.0', '1.11.4']

'''

import re
# The regex that locates version numbers and floats
num_re = re.compile(r'(\d+\.\d+\.\d+|[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)')
# The regex of the exponent
exp_re = re.compile(r'^[eE][-+]?[0-9]+$')
# Version regex
ver_re = re.compile(r'^\d+\.\d+\.\d+$')

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
    It also has basic support for version numbers.
    For use in passing to the :py:func:`sorted` builtin or
    :py:meth:`sort` attribute of lists.

        >>> a = ['num3', 'num5', 'num2']
        >>> a.sort(key=natsort_key)
        >>> a
        ['num2', 'num3', 'num5']
        >>> class Foo:
        ...    def __init__(self, bar):
        ...        self.bar = bar
        ...    def __repr__(self):
        ...        return "Foo('{0}')".format(self.bar)
        >>> b = [Foo('num3'), Foo('num5'), Foo('num2')]
        >>> b.sort(key=lambda x: natsort_key(x.bar))
        >>> b
        [Foo('num2'), Foo('num3'), Foo('num5')]
        >>> from operator import attrgetter
        >>> c = [Foo('num3'), Foo('num5'), Foo('num2')]
        >>> f = attrgetter('bar')
        >>> c.sort(key=lambda x: natsort_key(f(x)))
        >>> c
        [Foo('num2'), Foo('num3'), Foo('num5')]

    '''

    # If we are dealing with non-strings, return now
    if not isinstance(s, str):
        return (s,)

    # Split.  If there are no splits, return now
    s = num_re.split(s)
    if len(s) == 1:
        return tuple(s)

    # Remove all the None elements and exponentials from the list.
    # This results from the way split works when there are parenthesis
    # in the regular expression
    ix = [i for i, x in enumerate(s) if x is None or exp_re.match(x)]
    for i in reversed(ix):
        s.pop(i)

    # Try to remove empty strings
    try:
        s.remove('')
    except ValueError:
        pass

    # Now convert floats to floats and 
    # versions to tuples, i.e. 4.5.2 => (4, 5, 2)
    for i in xrange(len(s)):

        # The versions
        if ver_re.match(s[i]):
            s[i] = tuple([int(x) for x in s[i].split('.')])
        else:
            # Try to make an int
            try:
                s[i] = (int(s[i]),)
            except ValueError:
                # If an int doesn't work, try a float
                try:
                    s[i] = (float(s[i]),)
                # It's just a string, do nothing
                except ValueError:
                    pass

    # Now, convert this list to a tuple
    return tuple(s)

def natsorted(seq, key=None):
    '''\
    Sorts a sequence naturally (alphabetically and numerically),
    not by ASCII.

        >>> a = ['num3', 'num5', 'num2']
        >>> natsorted(a)
        ['num2', 'num3', 'num5']
        >>> class Foo:
        ...    def __init__(self, bar):
        ...        self.bar = bar
        ...    def __repr__(self):
        ...        return "Foo('{0}')".format(self.bar)
        >>> b = [Foo('num3'), Foo('num5'), Foo('num2')]
        >>> from operator import attrgetter
        >>> natsorted(b, key=attrgetter('bar'))
        [Foo('num2'), Foo('num3'), Foo('num5')]

    :argument seq:
        The sequence to be sorted.
    :type seq: sequence-like
    :rtype: list
    '''
    if key:
        return sorted(seq, key=lambda x: natsort_key(key(x)))
    else:
        return sorted(seq, key=natsort_key)

def index_natsorted(seq, key=lambda x: x):
    '''\
    Sorts a sequence naturally, but returns a list of sorted the 
    indeces and not the sorted list.

        >>> a = ['num3', 'num5', 'num2']
        >>> b = ['foo', 'bar', 'baz']
        >>> index = index_natsorted(a)
        >>> index
        [2, 0, 1]
        >>> # Sort both lists by the sort order of a
        >>> [a[i] for i in index]
        ['num2', 'num3', 'num5']
        >>> [b[i] for i in index]
        ['baz', 'foo', 'bar']
        >>> class Foo:
        ...    def __init__(self, bar):
        ...        self.bar = bar
        ...    def __repr__(self):
        ...        return "Foo('{0}')".format(self.bar)
        >>> c = [Foo('num3'), Foo('num5'), Foo('num2')]
        >>> from operator import attrgetter
        >>> index_natsorted(c, key=attrgetter('bar'))
        [2, 0, 1]

    :argument seq:
        The sequence that you want the sorted index of.
    :type seq: sequence-like
    :rtype: list
    '''
    from operator import itemgetter
    item1 = itemgetter(1)
    # Pair the index and sequence together, then sort by 
    index_seq_pair = [[x, key(y)] for x, y in zip(xrange(len(seq)), seq)]
    index_seq_pair.sort(key=lambda x: natsort_key(item1(x)))
    return [x[0] for x in index_seq_pair]

def test():
    from doctest import DocTestSuite
    return DocTestSuite()

# Test this module
if __name__ == '__main__':
    import doctest
    doctest.testmod()
