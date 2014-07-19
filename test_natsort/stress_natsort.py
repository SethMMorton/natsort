# -*- coding: utf-8 -*-
"""\
This file contains functions to stress-test natsort.
"""
from random import randint, sample, choice
from string import printable
from copy import copy
from pytest import fail
from natsort import natsorted
from natsort.py23compat import py23_range


def test_random():
    """Try to sort 100,000 randomly generated strings without exception."""

    # Repeat test 100,000 times
    for _ in py23_range(100000):
        # Made a list of five randomly generated strings
        lst = [''.join(sample(printable, randint(7, 30)))
               for __ in py23_range(5)]
        # Try to sort.  If there is an exception, give some detailed info.
        try:
            natsorted(lst)
        except Exception as e:
            msg = "Ended with exception type '{exc}: {msg}'.\n"
            msg += "Failed on the input {lst}."
            fail(msg.format(exc=type(e).__name__, msg=str(e), lst=str(lst)))


def test_similar():
    """Try to sort 100,000 randomly generated
    similar strings without exception.
    """

    # Repeat test 100,000 times
    for _ in py23_range(100000):
        # Create a randomly generated string
        base = sample(printable, randint(7, 30))
        # Make a list of strings based on this string,
        # with some randomly generated modifications
        lst = []
        for __ in py23_range(5):
            new_str = copy(base)
            for ___ in py23_range(randint(1, 5)):
                new_str[randint(0, len(base)-1)] = choice(printable)
            lst.append(''.join(new_str))
        # Try to sort.  If there is an exception, give some detailed info.
        try:
            natsorted(lst)
        except Exception as e:
            msg = "Ended with exception type '{exc}: {msg}'.\n"
            msg += "Failed on the input {lst}."
            fail(msg.format(exc=type(e).__name__, msg=str(e), lst=str(lst)))
