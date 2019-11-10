.. default-domain:: py
.. currentmodule:: natsort

.. _shell:

Shell Script
============

The ``natsort`` shell script is automatically installed when you install
:mod:`natsort` with pip.

Below is the usage and some usage examples for the ``natsort`` shell script.

Usage
-----

.. code-block::

    usage: natsort [-h] [--version] [-p] [-f LOW HIGH] [-F LOW HIGH] [-e EXCLUDE]
                   [-r] [-t {digit,int,float,version,ver}] [--nosign] [--noexp]
                   [--locale]
                   [entries [entries ...]]

    Performs a natural sort on entries given on the command-line.
    A natural sort sorts numerically then alphabetically, and will sort
    by numbers in the middle of an entry.

    positional arguments:
      entries               The entries to sort. Taken from stdin if nothing is
                            given on the command line.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -p, --paths           Interpret the input as file paths. This is not
                            strictly necessary to sort all file paths, but in
                            cases where there are OS-generated file paths like
                            "Folder/" and "Folder (1)/", this option is needed to
                            make the paths sorted in the order you expect
                            ("Folder/" before "Folder (1)/").
      -f LOW HIGH, --filter LOW HIGH
                            Used for keeping only the entries that have a number
                            falling in the given range.
      -F LOW HIGH, --reverse-filter LOW HIGH
                            Used for excluding the entries that have a number
                            falling in the given range.
      -e EXCLUDE, --exclude EXCLUDE
                            Used to exclude an entry that contains a specific
                            number.
      -r, --reverse         Returns in reversed order.
      -t {digit,int,float,version,ver,real,f,i,r,d},
      --number-type {digit,int,float,version,ver,real,f,i,r,d},
      --number_type {digit,int,float,version,ver,real,f,i,r,d}
                            Choose the type of number to search for. "float" will
                            search for floating-point numbers. "int" will only
                            search for integers. "digit", "version", and "ver" are
                            synonyms for "int"."real" is a shortcut for "float"
                            with --sign. "i" and "d" are synonyms for "int", "f"
                            is a synonym for "float", and "r" is a synonym for
                            "real".The default is int.
      --nosign              Do not consider "+" or "-" as part of a number, i.e.
                            do not take sign into consideration. This is the
                            default.
      -s, --sign            Consider "+" or "-" as part of a number, i.e. take
                            sign into consideration. The default is unsigned.
      --noexp               Do not consider an exponential as part of a number,
                            i.e. 1e4, would be considered as 1, "e", and 4, not as
                            10000. This only effects the --number-type=float.
      -l, --locale          Causes natsort to use locale-aware sorting. You will
                            get the best results if you install PyICU.

Description
-----------

``natsort`` was originally written to aid in computational chemistry
research so that it would be easy to analyze large sets of output files
named after the parameter used:

.. code-block:: console

    $ ls *.out
    mode1000.35.out mode1243.34.out mode744.43.out mode943.54.out

(Obviously, in reality there would be more files, but you get the idea.) Notice
that the shell sorts in lexicographical order.  This is the behavior of programs like
``find`` as well as ``ls``.  The problem is passing these files to an
analysis program causes them not to appear in numerical order, which can lead
to bad analysis.  To remedy this, use ``natsort``:

.. code-block:: console

    $ natsort *.out
    mode744.43.out
    mode943.54.out
    mode1000.35.out
    mode1243.34.out
    $ natsort -t r *.out | xargs your_program

``-t r`` is short for ``--number-type real``. You can also place natsort in
the middle of a pipe:

.. code-block:: console

    $ find . -name "*.out" | natsort -t r | xargs your_program

To sort version numbers, use the default ``--number-type``:

.. code-block:: console

    $ ls *
    prog-1.10.zip prog-1.9.zip prog-2.0.zip
    $ natsort *
    prog-1.9.zip
    prog-1.10.zip
    prog-2.0.zip

In general, all ``natsort`` shell script options mirror the :func:`~natsorted`
API, with notable exception of the ``--filter``, ``--reverse-filter``, and ``--exclude``
options.  These three options are used as follows:

.. code-block:: console

    $ ls *.out
    mode1000.35.out mode1243.34.out mode744.43.out mode943.54.out
    $ natsort -t r *.out -f 900 1100 # Select only numbers between 900-1100
    mode943.54.out
    mode1000.35.out
    $ natsort -t r *.out -F 900 1100 # Select only numbers NOT between 900-1100
    mode744.43.out
    mode1243.34.out
    $ natsort -t r *.out -e 1000.35 # Exclude 1000.35 from search
    mode744.43.out
    mode943.54.out
    mode1243.34.out

If you are sorting paths with OS-generated filenames, you may require the
``--paths``/``-p`` option:

.. code-block:: console

    $ find . ! -path . -type f
    ./folder/file (1).txt
    ./folder/file.txt
    ./folder (1)/file.txt
    ./folder (10)/file.txt
    ./folder (2)/file.txt
    $ find . ! -path . -type f | natsort
    ./folder (1)/file.txt
    ./folder (2)/file.txt
    ./folder (10)/file.txt
    ./folder/file (1).txt
    ./folder/file.txt
    $ find . ! -path . -type f | natsort -p
    ./folder/file.txt
    ./folder/file (1).txt
    ./folder (1)/file.txt
    ./folder (2)/file.txt
    ./folder (10)/file.txt
