# -*- coding: utf-8 -*-
from __future__ import (print_function, division,
                        unicode_literals, absolute_import)

import functools
import sys

# These functions are used to make the doctests compatible between
# python2 and python3.  This code is pretty much lifted from the iPython
# project's py3compat.py file.  Credit to the iPython devs.

# Assume all strings are Unicode in Python 2
py23_str = str if sys.version[0] == '3' else unicode

# Use the range iterator always
py23_range = range if sys.version[0] == '3' else xrange

# Uniform base string type
py23_basestring = str if sys.version[0] == '3' else basestring

# zip as an iterator
if sys.version[0] == '3':
    py23_zip = zip
else:
    import itertools
    py23_zip = itertools.izip


# This function is intended to decorate other functions that will modify
# either a string directly, or a function's docstring.
def _modify_str_or_docstring(str_change_func):
    @functools.wraps(str_change_func)
    def wrapper(func_or_str):
        if isinstance(func_or_str, py23_basestring):
            func = None
            doc = func_or_str
        else:
            func = func_or_str
            doc = func.__doc__

        doc = str_change_func(doc)

        if func:
            func.__doc__ = doc
            return func
        return doc
    return wrapper


# Properly modify a doctstring to either have the unicode literal or not.
if sys.version[0] == '3':
    # Abstract u'abc' syntax:
    @_modify_str_or_docstring
    def u_format(s):
        """"{u}'abc'" --> "'abc'" (Python 3)

        Accepts a string or a function, so it can be used as a decorator."""
        return s.format(u='')
else:
    # Abstract u'abc' syntax:
    @_modify_str_or_docstring
    def u_format(s):
        """"{u}'abc'" --> "u'abc'" (Python 2)

        Accepts a string or a function, so it can be used as a decorator."""
        return s.format(u='u')
