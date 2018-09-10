"""
Fixtures for pytest.
"""

import locale

import pytest


def load_locale(x):
    """Convenience to load a locale, trying ISO8859-1 first."""
    try:
        locale.setlocale(locale.LC_ALL, str("{0}.ISO8859-1".format(x)))
    except locale.Error:
        locale.setlocale(locale.LC_ALL, str("{0}.UTF-8".format(x)))


@pytest.fixture()
def with_locale_en_us():
    """Convenience to load the en_US locale - reset when complete."""
    orig = locale.getlocale()
    yield load_locale("en_US")
    locale.setlocale(locale.LC_ALL, orig)


@pytest.fixture()
def with_locale_de_de():
    """
    Convenience to load the de_DE locale - reset when complete - skip if missing.
    """
    orig = locale.getlocale()
    try:
        load_locale("de_DE")
    except locale.Error:
        pytest.skip("requires de_DE locale to be installed")
    else:
        yield
    finally:
        locale.setlocale(locale.LC_ALL, orig)
