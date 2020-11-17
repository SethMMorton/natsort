# -*- coding: utf-8 -*-
"""
Testing for the OS sorting
"""
import platform

import natsort
import pytest

try:
    import icu  # noqa: F401
except ImportError:
    has_icu = False
else:
    has_icu = True


def test_os_sorted_compound():
    given = [
        "/p/Folder (10)/file.tar.gz",
        "/p/Folder (1)/file (1).tar.gz",
        "/p/Folder/file.x1.9.tar.gz",
        "/p/Folder (2)/file.tar.gz",
        "/p/Folder (1)/file.tar.gz",
        "/p/Folder/file.x1.10.tar.gz",
    ]
    expected = [
        "/p/Folder/file.x1.9.tar.gz",
        "/p/Folder/file.x1.10.tar.gz",
        "/p/Folder (1)/file.tar.gz",
        "/p/Folder (1)/file (1).tar.gz",
        "/p/Folder (2)/file.tar.gz",
        "/p/Folder (10)/file.tar.gz",
    ]
    result = natsort.os_sorted(given)
    assert result == expected


def test_os_sorted_misc_no_fail():
    natsort.os_sorted([9, 4.3, None, float("nan")])


# The following is a master list of things that might give trouble
# when sorting like the file explorer.
given = [
    "11111",
    "!",
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "+",
    "+11111",
    "+aaaaa",
    ",",
    "-",
    ";",
    "=",
    "@",
    "[",
    "]",
    "^",
    "_",
    "`",
    "aaaaa",
    "foo0",
    "foo_0",
    "{",
    "}",
    "~",
    "§",
    "°",
    "´",
    "µ",
    "€",
    "foo1",
    "foo2",
    "foo4",
    "foo10",
    "Foo3",
]

# The expceted values change based on the environment
if platform.system() == "Windows":
    expected = [
        "'",
        "-",
        "!",
        "#",
        "$",
        "%",
        "&",
        "(",
        ")",
        ",",
        ";",
        "@",
        "[",
        "]",
        "^",
        "_",
        "`",
        "{",
        "}",
        "~",
        "´",
        "€",
        "+",
        "+11111",
        "+aaaaa",
        "=",
        "§",
        "°",
        "µ",
        "11111",
        "aaaaa",
        "foo_0",
        "foo0",
        "foo1",
        "foo2",
        "Foo3",
        "foo4",
        "foo10",
    ]

elif has_icu:
    expected = [
        "_",
        "-",
        ",",
        ";",
        "!",
        "'",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "§",
        "@",
        "&",
        "#",
        "%",
        "`",
        "´",
        "^",
        "°",
        "+",
        "+11111",
        "+aaaaa",
        "=",
        "~",
        "$",
        "€",
        "11111",
        "aaaaa",
        "foo_0",
        "foo0",
        "foo1",
        "foo2",
        "Foo3",
        "foo4",
        "foo10",
        "µ",
    ]
else:
    # For non-ICU UNIX, the order is all over the place
    # from platform to platform, distribution to distribution.
    # It's not really possible to predict the order across all
    # the different OS. To work around this, we will exclude
    # the special characters from the sort.
    given = given[0:1] + given[22:25] + given[33:]
    expected = [
        "11111",
        "aaaaa",
        "foo0",
        "foo1",
        "foo2",
        "Foo3",
        "foo4",
        "foo10",
        "foo_0",
    ]


@pytest.mark.usefixtures("with_locale_en_us")
def test_os_sorted_corpus():
    result = natsort.os_sorted(given)
    print(result)
    assert result == expected
