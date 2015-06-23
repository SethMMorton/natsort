from __future__ import absolute_import

import locale


def load_locale(x):
    try:
        locale.setlocale(locale.LC_ALL, str('{}.ISO8859-1'.format(x)))
    except:
        locale.setlocale(locale.LC_ALL, str('{}.UTF-8'.format(x)))

try:
    load_locale('de_DE')
    has_locale_de_DE = True
except locale.Error:
    has_locale_de_DE = False
