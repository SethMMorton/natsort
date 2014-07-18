# -*- coding: utf-8 -*-
"""\
Test the natsort command-line tool functions.
"""
import re
import sys
from pytest import raises
from natsort.__main__ import main, range_check, check_filter
from natsort.__main__ import keep_entry_range, exclude_entry
from natsort.__main__ import sort_and_print_entries


def test_main(capsys):

    # Simple sorting
    sys.argv[1:] = ['num-2', 'num-6', 'num-1']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
num-6
num-2
num-1
"""

    # Reverse order
    sys.argv[1:] = ['-r', 'num-2', 'num-6', 'num-1']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
num-1
num-2
num-6
"""

    # Neglect '-' or '+'
    sys.argv[1:] = ['--nosign', 'num-2', 'num-6', 'num-1']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
num-1
num-2
num-6
"""

    # Sort as digits
    sys.argv[1:] = ['-t', 'digit', 'num-2', 'num-6', 'num-1']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
num-1
num-2
num-6
"""

    # Sort as versions (synonym for digits)
    sys.argv[1:] = ['-t', 'version', 'num-2', 'num-6', 'num-1']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
num-1
num-2
num-6
"""

    # Exclude the number -1 and 6.  Only -1 is present.
    sys.argv[1:] = ['-t', 'int', '-e', '-1', '-e', '6',
                    'num-2', 'num-6', 'num-1']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
num-6
num-2
"""

    # Exclude the number 1 and 6.
    # Both are present because we use digits/versions.
    sys.argv[1:] = ['-t', 'ver', '-e', '1', '-e', '6',
                    'num-2', 'num-6', 'num-1']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
num-2
"""

    # Floats work too.
    sys.argv[1:] = ['a1.0e3', 'a5.3', 'a453.6']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
a5.3
a453.6
a1.0e3
"""

    # Only include in the range of 1-10.
    sys.argv[1:] = ['-f', '1', '10', 'a1.0e3', 'a5.3', 'a453.6']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
a5.3
"""

    # Don't include in the range of 1-10.
    sys.argv[1:] = ['-F', '1', '10', 'a1.0e3', 'a5.3', 'a453.6']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
a453.6
a1.0e3
"""

    # Include two ranges.
    sys.argv[1:] = ['-f', '1', '10', '-f', '400', '500',
                    'a1.0e3', 'a5.3', 'a453.6']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
a5.3
a453.6
"""

    # Don't account for exponential notation.
    sys.argv[1:] = ['--noexp', 'a1.0e3', 'a5.3', 'a453.6']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
a1.0e3
a5.3
a453.6
"""

    # To sort complicated filenames you need --paths
    sys.argv[1:] = ['/Folder (1)/', '/Folder/', '/Folder (10)/']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
/Folder (1)/
/Folder (10)/
/Folder/
"""
    sys.argv[1:] = ['--paths', '/Folder (1)/', '/Folder/', '/Folder (10)/']
    main()
    out, __ = capsys.readouterr()
    assert out == """\
/Folder/
/Folder (1)/
/Folder (10)/
"""


def test_range_check():

    # Floats are always returned
    assert range_check(10, 11) == (10.0, 11.0)
    assert range_check(6.4, 30) == (6.4, 30.0)

    # Invalid ranges give a ValueErro
    with raises(ValueError) as err:
        range_check(7, 2)
    assert str(err.value) == 'low >= high'


def test_check_filter():

    # No filter gives 'None'
    assert check_filter(()) is None
    assert check_filter(False) is None
    assert check_filter(None) is None

    # The check filter always returns floats
    assert check_filter([(6, 7)]) == [(6.0, 7.0)]
    assert check_filter([(6, 7), (2, 8)]) == [(6.0, 7.0), (2.0, 8.0)]

    # Invalid ranges get a ValueError
    with raises(ValueError) as err:
        check_filter([(7, 2)])
    assert str(err.value) == 'Error in --filter: low >= high'


def test_keep_entry_range():

    regex = re.compile(r'\d+')
    assert keep_entry_range('a56b23c89', [0], [100], int, regex)
    assert keep_entry_range('a56b23c89', [1, 88], [20, 90], int, regex)
    assert not keep_entry_range('a56b23c89', [1], [20], int, regex)


def test_exclude_entry():

    # Check if the exclude value is present in the input string
    regex = re.compile(r'\d+')
    assert exclude_entry('a56b23c89', [100, 45], int, regex)
    assert not exclude_entry('a56b23c89', [23], int, regex)


def test_sort_and_print_entries(capsys):

    class Args:
        """A dummy class to simulate the argparse Namespace object"""
        def __init__(self, filter, reverse_filter, exclude, as_path, reverse):
            self.filter = filter
            self.reverse_filter = reverse_filter
            self.exclude = exclude
            self.reverse = reverse
            self.number_type = 'float'
            self.signed = True
            self.exp = True
            self.paths = as_path

    entries = ['tmp/a57/path2',
               'tmp/a23/path1',
               'tmp/a1/path1',
               'tmp/a1 (1)/path1',
               'tmp/a130/path1',
               'tmp/a64/path1',
               'tmp/a64/path2']

    # Just sort the paths
    sort_and_print_entries(entries, Args(None, None, False, False, False))
    out, __ = capsys.readouterr()
    assert out == """\
tmp/a1 (1)/path1
tmp/a1/path1
tmp/a23/path1
tmp/a57/path2
tmp/a64/path1
tmp/a64/path2
tmp/a130/path1
"""

    # You would use --paths to make them sort
    # as paths when the OS makes duplicates
    sort_and_print_entries(entries, Args(None, None, False, True, False))
    out, __ = capsys.readouterr()
    assert out == """\
tmp/a1/path1
tmp/a1 (1)/path1
tmp/a23/path1
tmp/a57/path2
tmp/a64/path1
tmp/a64/path2
tmp/a130/path1
"""

    # Sort the paths with numbers between 20-100
    sort_and_print_entries(entries, Args([(20, 100)], None, False,
                                         False, False))
    out, __ = capsys.readouterr()
    assert out == """\
tmp/a23/path1
tmp/a57/path2
tmp/a64/path1
tmp/a64/path2
"""

    # Sort the paths without numbers between 20-100
    sort_and_print_entries(entries, Args(None, [(20, 100)], False,
                                         True, False))
    out, __ = capsys.readouterr()
    assert out == """\
tmp/a1/path1
tmp/a1 (1)/path1
tmp/a130/path1
"""

    # Sort the paths, excluding 23 and 130
    sort_and_print_entries(entries, Args(None, None, [23, 130], True, False))
    out, __ = capsys.readouterr()
    assert out == """\
tmp/a1/path1
tmp/a1 (1)/path1
tmp/a57/path2
tmp/a64/path1
tmp/a64/path2
"""

    # Sort the paths, excluding 2
    sort_and_print_entries(entries, Args(None, None, [2], False, False))
    out, __ = capsys.readouterr()
    assert out == """\
tmp/a1 (1)/path1
tmp/a1/path1
tmp/a23/path1
tmp/a64/path1
tmp/a130/path1
"""

    # Sort in reverse order
    sort_and_print_entries(entries, Args(None, None, False, True, True))
    out, __ = capsys.readouterr()
    assert out == """\
tmp/a130/path1
tmp/a64/path2
tmp/a64/path1
tmp/a57/path2
tmp/a23/path1
tmp/a1 (1)/path1
tmp/a1/path1
"""
