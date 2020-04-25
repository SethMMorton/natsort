.. default-domain:: py
.. currentmodule:: natsort

.. _howitworks:

How Does Natsort Work?
======================

.. contents::
    :local:

:mod:`natsort` works by breaking strings into smaller sub-components (numbers
or everything else), and returning these components in a tuple. Sorting
tuples in Python is well-defined, and this fact is used to sort the input
strings properly. But how does one break a string into sub-components?
And what does one do to those components once they are split? Below I
will explain the algorithm that was chosen for the :mod:`natsort` module,
and some of the thinking that went into those design decisions. I will
also mention some of the stumbling blocks I ran into because
`getting sorting right is surprisingly hard`_.

If you are impatient, you can skip to :ref:`tldr1` for the algorithm
in the simplest case, and :ref:`tldr2`
to see what extra code is needed to handle special cases.

First, How Does Natural Sorting Work At a High Level?
-----------------------------------------------------

If I want to compare '2 ft 7 in' to '2 ft 11 in', I might do the following

.. code-block:: pycon

    >>> '2 ft 7 in' < '2 ft 11 in'
    False

We as humans know that the above should be true, but why does Python think it
is false?  Here is how it is performing the comparison:

::

    '2' <=> '2' ==> equal, so keep going
    ' ' <=> ' ' ==> equal, so keep going
    'f' <=> 'f' ==> equal, so keep going
    't' <=> 't' ==> equal, so keep going
    ' ' <=> ' ' ==> equal, so keep going
    '7' <=> '1' ==> different, use result of '7' < '1'

'7' evaluates as greater than '1' so the statement is false. When sorting, if
a value is less than another it is placed first, so in our above example
'2 ft 11 in' would end up before '2 ft 7 in', which is not correct. What to do?

The best way to handle this is to break the string into sub-components
of numbers and non-numbers, and then convert the numeric parts into
:func:`float` or :func:`int` types. This will force Python to
actually understand the context of what it is sorting and then "do the
right thing." Luckily, it handles sorting lists of strings right
out-of-the-box, so the only hard part is actually making this string-to-list
transformation and then Python will handle the rest.

::

    '2 ft 7 in'  ==> (2, ' ft ', 7,  ' in')
    '2 ft 11 in' ==> (2, ' ft ', 11, ' in')

When Python compares the two, it roughly follows the below logic:

::

    2       <=> 2      ==> equal, so keep going
    ' ft '  <=> ' ft ' ==> a string is a special type of sequence - evaluate each character individually
                       ||
                       -->
                          ' ' <=> ' ' ==> equal, so keep going
                          'f' <=> 'f' ==> equal, so keep going
                          't' <=> 't' ==> equal, so keep going
                          ' ' <=> ' ' ==> equal, so keep going
                      <== Back to parent sequence
    7 <=> 11 ==> different, use the result of 7 < 11

Clearly, seven is less than eleven, so our comparison is as we expect, and we
would get the sorting order we wanted.

At its heart, :mod:`natsort` is simply a tool to break strings into tuples,
turning numbers in strings (i.e. ``'79'``) into *ints* and *floats* as it does this.

Natsort's Approach
------------------

.. contents::
    :local:

Decomposing Strings Into Sub-Components
+++++++++++++++++++++++++++++++++++++++

The first major hurtle to overcome is to decompose the string into
sub-components. Remarkably, this turns out to be the easy part, owing mostly
to Python's easy access to regular expressions. Breaking an arbitrary string
based on a pattern is pretty straightforward.

.. code-block:: pycon

    >>> import re
    >>> re.split(r'(\d+)', '2 ft 11 in')
    ['', '2', ' ft ', '11', ' in']

Clear (assuming you can read regular expressions) and concise.

The reason I began developing :mod:`natsort` in the first place was because I
needed to handle the natural sorting of strings containing *real numbers*, not
just unsigned integers as the above example contains. By real numbers, I mean
those like ``-45.4920E-23``. :mod:`natsort` can handle just about any number
definition; to that end, here are all the regular expressions used in
:mod:`natsort`:

.. code-block:: pycon

    >>> unsigned_int               = r'([0-9]+)'
    >>> signed_int                 = r'([-+]?[0-9]+)'
    >>> unsigned_float             = r'((?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][-+]?[0-9]+)?)'
    >>> signed_float               = r'([-+]?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE][-+]?[0-9]+)?)'
    >>> unsigned_float_no_exponent = r'((?:[0-9]+\.?[0-9]*|\.[0-9]+))'
    >>> signed_float_no_exponent   = r'([-+]?(?:[0-9]+\.?[0-9]*|\.[0-9]+))'

Note that ``"inf"`` and ``"nan"`` are deliberately omitted from the float
definition because you wouldn't want (for example) ``"banana"`` to be converted
into ``['ba', 'nan', 'a']``, Let's see an example:

.. code-block:: pycon

    >>> re.split(signed_float, 'The mass of 3 electrons is 2.732815068E-30 kg')
    ['The mass of ', '3', ' electrons is ', '2.732815068E-30', ' kg']

.. note::

    It is a bit of a lie to say the above are the complete regular expressions. In the
    actual code there is also handling for non-ASCII unicode characters (such as ⑦),
    but I will ignore that aspect of :mod:`natsort` in this discussion.

Now, when the user wants to change the definition of a number, it is as easy as
changing the pattern supplied to the regular expression engine.

Choosing the right default is hard, though (well, in this case it shouldn't
have been but I was rather thick-headed). In retrospect, it should have been
obvious that since essentially all the code examples I had/have seen for
natural sorting were for *unsigned integers*, I should have made the default
definition of a number an *unsigned integer*. But, in the brash days of my
youth I assumed that since my use case was real numbers, everyone else would
be happier sorting by real numbers; so, I made the default definition of a
number a *signed float with exponent*. `This astonished`_ `a lot`_ `of people`_
(`and some people aren't very nice when they are astonished`_).
Starting with :mod:`natsort` version 4.0.0 the default number definition was
changed to an *unsigned integer* which satisfies the "least astonishment"
principle, and I have not heard a complaint since.

Coercing Strings Containing Numbers Into Numbers
++++++++++++++++++++++++++++++++++++++++++++++++

There has been some debate on Stack Overflow as to what method is best to
coerce a string to a number if it can be coerced, and leaving it alone otherwise
(see `this one for coercion`_ and `this one for checking`_ for some high traffic questions),
but it mostly boils down to two different solutions, shown here:

.. code-block:: pycon

    >>> def coerce_try_except(x):
    ...     try:
    ...         return int(x)
    ...     except ValueError:
    ...         return x
    ...
    >>> def coerce_regex(x):
    ...     # Note that precompiling the regex is more performant,
    ...     # but I do not show that here for clarity's sake.
    ...     return int(x) if re.match(r'[-+]?\d+$', x) else x
    ...

Here are some timing results run on my machine:

.. code-block:: pycon

    In [0]: numbers = list(map(str, range(100)))  # A list of numbers as strings

    In [1]: not_numbers = ['banana' + x for x in numbers]

    In [2]: %timeit [coerce_try_except(x) for x in numbers]
    10000 loops, best of 3: 51.1 µs per loop

    In [3]: %timeit [coerce_try_except(x) for x in not_numbers]
    1000 loops, best of 3: 289 µs per loop

    In [4]: %timeit [coerce_regex(x) for x in not_numbers]
    10000 loops, best of 3: 67.6 µs per loop

    In [5]: %timeit [coerce_regex(x) for x in numbers]
    10000 loops, best of 3: 123 µs per loop

What can we learn from this? The ``try: except`` method (arguably the most
"pythonic" of the solutions) is best for numeric input, but performs over 5X
slower for non-numeric input. Conversely, the regular expression method, though
slower than ``try: except`` for both input types, is more efficient for
non-numeric input than for input that can be converted to an ``int``. Further,
even though the regular expression method is slower for both input types, it is
always at least twice as fast as the worst case for the ``try: except``.

Why do I care? Shouldn't I just pick a method and not worry about it? Probably.
However, I am very conscious about the performance of :mod:`natsort`, and want
it to be a true drop-in replacement for :func:`sorted` without having to incur
a performance penalty. For the purposes of :mod:`natsort`, there is no clear
winner between the two algorithms - the data being passed to this function will
likely be a mix of numeric and non-numeric string content. Do I use the
``try: except`` method and hope the speed gains on numbers will offset the
non-number performance, or do I use regular expressions and take the more
stable performance?

It turns out that within the context of :mod:`natsort`, some assumptions can be
made that make a hybrid approach attractive. Because all strings are pre-split
into numeric and non-numeric content *before* being passed to this coercion
function, the assumption can be made that *if a string begins with a digit or a
sign, it can be coerced into a number*.

.. code-block:: pycon

    >>> def coerce_to_int(x):
    ...     if x[0] in '0123456789+-':
    ...         try:
    ...             return int(x)
    ...         except ValueError:
    ...             return x
    ...     else:
    ...         return x
    ...

So how does this perform compared to the standard coercion methods?

.. code-block:: pycon

    In [6]: %timeit [coerce_to_int(x) for x in numbers]
    10000 loops, best of 3: 71.6 µs per loop

    In [7]: %timeit [coerce_to_int(x) for x in not_numbers]
    10000 loops, best of 3: 26.4 µs per loop

The hybrid method eliminates most of the time wasted on numbers checking
that it is in fact a number before passing to :func:`int`, and eliminates
the time wasted in the exception stack for input that is not a number.

That's as fast as we can get, right? In pure Python, probably. At least, it's
close. But because I am crazy and a glutton for punishment, I decided to see
if I could get any faster writing a C extension. It's called
`fastnumbers`_ and contains a C implementation of the above coercion functions
called :func:`fast_int`. How does it fair? Pretty well.

.. code-block:: pycon

    In [8]: %timeit [fast_int(x) for x in numbers]
    10000 loops, best of 3: 30.9 µs per loop

    In [9]: %timeit [fast_int(x) for x in not_numbers]
    10000 loops, best of 3: 30 µs per loop

During development of :mod:`natsort`, I wanted to ensure that using it did not
get in the way of a user's program by introducing a performance penalty to
their code. To that end, I do not feel like my adventures down the rabbit hole
of optimization of coercion functions was a waste; I can confidently look users
in the eye and say I considered every option in ensuring :mod:`natsort` is as
efficient as possible. This is why if `fastnumbers`_ is installed it will be
used for this step, and otherwise the hybrid method will be used.

.. note::

    Modifying the hybrid coercion function for floats is straightforward.

    .. code-block:: pycon

        >>> def coerce_to_float(x):
        ...     if x[0] in '.0123456789+-' or x.lower().lstrip()[:3] in ('nan', 'inf'):
        ...         try:
        ...             return float(x)
        ...         except ValueError:
        ...             return x
        ...     else:
        ...         return x
        ...

.. _tldr1:

TL;DR 1 - The Simple "No Special Cases" Algorithm
+++++++++++++++++++++++++++++++++++++++++++++++++

At this point, our :mod:`natsort` algorithm is essentially the following:

.. code-block:: pycon

    >>> import re
    >>> def natsort_key(x, as_float=False, signed=False):
    ...     if as_float:
    ...         regex = signed_float if signed else unsigned_float
    ...     else:
    ...         regex = signed_int if signed else unsigned_int
    ...     split_input = re.split(regex, x)
    ...     split_input = filter(None, split_input)  # removes null strings
    ...     coerce = coerce_to_float if as_float else coerce_to_int
    ...     return tuple(coerce(s) for s in split_input)
    ...

I have written the above for clarity and not performance.
This pretty much matches `most natural sort solutions for python on Stack Overflow`_
(except the above includes customization of the definition of a number).

Special Cases Everywhere!
-------------------------

.. contents::
    :local:

.. image:: special_cases_everywhere.jpg

If what I described in :ref:`TL;DR 1 <tldr1>` were
all that :mod:`natsort` needed to
do then there probably wouldn't be much need for a third-party module, right?
Probably. But it turns out that in real-world data there are a lot of
special cases that need to be handled, and in true `80%/20%`_ fashion, the
majority of the code in :mod:`natsort` is devoted to handling special cases
like those described below.

Sorting Filesystem Paths
++++++++++++++++++++++++

`The first major special case I encountered was sorting filesystem paths`_
(if you go to the link, you will see I didn't handle it well for a year...
this was before I fully realized how much functionality I could really add
to :mod:`natsort`). Let's apply the :func:`natsort_key` from above to some
filesystem paths that you might see being auto-generated from your operating
system:

.. code-block:: pycon

    >>> paths = ['Folder (10)/file.tar.gz',
    ...          'Folder/file.tar.gz',
    ...          'Folder (1)/file (1).tar.gz',
    ...          'Folder (1)/file.tar.gz']
    >>> sorted(paths, key=natsort_key)
    ['Folder (1)/file (1).tar.gz', 'Folder (1)/file.tar.gz', 'Folder (10)/file.tar.gz', 'Folder/file.tar.gz']

Well that's not right! What is ``'Folder/file.tar.gz'`` doing at the end?
It has to do with the numerical ASCII code assigned to the space and
``/`` characters in the `ASCII table`_. According to the `ASCII table`_, the
space character (number 32) comes before the ``/`` character (number 47). If
we remove the common prefix in all of the above strings (``'Folder'``), we
can see why this happens:

.. code-block:: pycon

    >>> ' (1)/file.tar.gz' < '/file.tar.gz'
    True
    >>> ' ' < '/'
    True

This isn't very convenient... how do we solve it? We can split the path
across the path separators and then sort. A convenient way do to this is
with the :data:`Path.parts <pathlib.PurePath.parts>` property from
:mod:`pathlib`:

.. code-block:: pycon

    >>> import pathlib
    >>> sorted(paths, key=lambda x: tuple(natsort_key(s) for s in pathlib.Path(x).parts))
    ['Folder/file.tar.gz', 'Folder (1)/file (1).tar.gz', 'Folder (1)/file.tar.gz', 'Folder (10)/file.tar.gz']

Almost! It seems like there is some funny business going on in the final
filename component as well. We can solve that nicely and quickly with
:data:`Path.suffixes <pathlib.PurePath.suffixes>` and :data:`Path.stem
<pathlib.PurePath.stem>`.

.. code-block:: pycon

    >>> def decompose_path_into_components(x):
    ...     path_split = list(pathlib.Path(x).parts)
    ...     # Remove the final filename component from the path.
    ...     final_component = pathlib.Path(path_split.pop())
    ...     # Split off all the extensions.
    ...     suffixes = final_component.suffixes
    ...     stem = final_component.name.replace(''.join(suffixes), '')
    ...     # Remove the '.' prefix of each extension, and make that
    ...     # final component a list of the stem and each suffix.
    ...     final_component = [stem] + [x[1:] for x in suffixes]
    ...     # Replace the split final filename component.
    ...     path_split.extend(final_component)
    ...     return path_split
    ...
    >>> def natsort_key_with_path_support(x):
    ...     return tuple(natsort_key(s) for s in decompose_path_into_components(x))
    ...
    >>> sorted(paths, key=natsort_key_with_path_support)
    ['Folder/file.tar.gz', 'Folder (1)/file.tar.gz', 'Folder (1)/file (1).tar.gz', 'Folder (10)/file.tar.gz']

This works because in addition to breaking the input by path separators,
the final filename component is separated from its extensions as well.
*Then*, each of these separated components is sent to the
:mod:`natsort` algorithm, so the result is a tuple of tuples. Once that
is done, we can see how comparisons can be done in the expected manner.

.. code-block:: pycon

    >>> a = natsort_key_with_path_support('Folder (1)/file (1).tar.gz')
    >>> a
    (('Folder (', 1, ')'), ('file (', 1, ')'), ('tar',), ('gz',))
    >>>
    >>> b = natsort_key_with_path_support('Folder/file.tar.gz')
    >>> b
    (('Folder',), ('file',), ('tar',), ('gz',))
    >>>
    >>> a > b
    True

Comparing Different Types on Python 3
+++++++++++++++++++++++++++++++++++++

`The second major special case I encountered was sorting of different types`_.
If you are on Python 2 (i.e. legacy Python), this mostly doesn't matter *too*
much since it uses an arbitrary heuristic to allow traditionally un-comparable
types to be compared (such as comparing ``'a'`` to ``1``). However, on Python 3
(i.e. Python) it simply won't let you perform such nonsense, raising a
:exc:`TypeError` instead.

You can imagine that a module that breaks strings into tuples of numbers and
strings is walking a dangerous line if it does not have special handling for
comparing numbers and strings. My imagination was not so great at first.
Let's take a look at all the ways this can fail with real-world data.

.. code-block:: pycon

    >>> def natsort_key_with_poor_real_number_support(x):
    ...     split_input = re.split(signed_float, x)
    ...     split_input = filter(None, split_input)  # removes null strings
    ...     return tuple(coerce_to_float(s) for s in split_input)
    >>>
    >>> sorted([5, '4'], key=natsort_key_with_poor_real_number_support)
    Traceback (most recent call last):
        ...
    TypeError: ...
    >>>
    >>> sorted(['12 apples', 'apples'], key=natsort_key_with_poor_real_number_support)
    Traceback (most recent call last):
        ...
    TypeError: ...
    >>>
    >>> sorted(['version5.3.0', 'version5.3rc1'], key=natsort_key_with_poor_real_number_support)
    Traceback (most recent call last):
        ...
    TypeError: ...

Let's break these down.

#. The integer ``5`` is sent to ``re.split`` which expects only strings
   or bytes, which is a no-no.
#. ``natsort_key_with_poor_real_number_support('12 apples') < natsort_key_with_poor_real_number_support('apples')``
   is the same as ``(12.0, ' apples') < ('apples',)``, and thus a number gets
   compared to a string [#f1]_ which also is a no-no.
#. This one scores big on the astonishment scale, especially if one
   accidentally uses signed integers or real numbers when they mean
   to use unsigned integers.
   ``natsort_key_with_poor_real_number_support('version5.3.0') < natsort_key_with_poor_real_number_support('version5.3rc1')``
   is the same as ``('version', 5.3, 0.0) < ('version', 5.3, 'rc', 1.0)``,
   so in the third element a number gets compared to a string, once again
   the same old no-no. (The same would happen with ``'version5-3'`` and
   ``'version5-a'``, which would become ``('version', 5, -3)`` and
   ``('version', 5, '-a')``).

As you might expect, the solution to the first issue is to wrap the
``re.split`` call in a ``try: except:`` block and handle the number specially
if a :exc:`TypeError` is raised. The second and third cases *could* be handled
in a "special case" manner, meaning only respond and do something different
if these problems are detected. But a less error-prone method is to ensure
that the data is correct-by-construction, and this can be done by ensuring
that the returned tuples *always* start with a string, and then alternate
in a string-number-string-number-string pattern; this can be achieved by
adding an empty string wherever the pattern is not followed [#f2]_. This ends
up working out pretty nicely because empty strings are always "less" than
any non-empty string, and we typically want numbers to come before strings.

Let's take a look at how this works out.

.. code-block:: pycon

    >>> from natsort.utils import sep_inserter
    >>> list(sep_inserter(iter(['apples']), ''))
    ['apples']
    >>>
    >>> list(sep_inserter(iter([12, ' apples']), ''))
    ['', 12, ' apples']
    >>>
    >>> list(sep_inserter(iter(['version', 5, -3]), ''))
    ['version', 5, '', -3]
    >>>
    >>> from natsort import natsort_keygen, ns
    >>> natsort_key_with_good_real_number_support = natsort_keygen(alg=ns.REAL)
    >>>
    >>> sorted([5, '4'], key=natsort_key_with_good_real_number_support)
    ['4', 5]
    >>>
    >>> sorted(['12 apples', 'apples'], key=natsort_key_with_good_real_number_support)
    ['12 apples', 'apples']
    >>>
    >>> sorted(['version5.3.0', 'version5.3rc1'], key=natsort_key_with_good_real_number_support)
    ['version5.3.0', 'version5.3rc1']

How the "good" version works will be given in
`TL;DR 2 - Handling Crappy, Real-World Input`_.

Handling NaN
++++++++++++

`A rather unexpected special case I encountered was sorting collections containing NaN`_.
Let's see what happens when you try to sort a plain old list of numbers when there
is a **NaN** floating around in there.

.. code-block:: pycon

    >>> danger = [7, float('nan'), 22.7, 19, -14, 59.123, 4]
    >>> sorted(danger)
    [7, nan, -14, 4, 19, 22.7, 59.123]

Clearly that isn't correct, and for once it isn't my fault!
`It's hard to compare floating point numbers`_. By definition, **NaN** is unorderable
to any other number, and is never equal to any other number, including itself.

.. code-block:: pycon

    >>> nan = float('nan')
    >>> 5 > nan
    False
    >>> 5 < nan
    False
    >>> 5 == nan
    False
    >>> 5 != nan
    True
    >>> nan == nan
    False
    >>> nan != nan
    True

The implication of all this for us is that if there is an **NaN** in the
data-set we are trying to sort, the data-set will end up being sorted in
two separate yet individually sorted sequences - the one *before* the **NaN**,
and the one *after*. This is because the ``<`` operation that is used
to sort always returns :const:`False` with **NaN**.

Because :mod:`natsort` aims to sort sequences in a way that does not surprise
the user, keeping this behavior is not acceptable (I don't require my users
to know how **NaN** will behave in a sorting algorithm). The simplest way to
satisfy the "least astonishment" principle is to substitute **NaN** with
some other value. But what value is *least* astonishing? I chose to replace
**NaN** with :math:`-\infty` so that these poorly behaved elements always
end up at the front where the users will most likely be alerted to their
presence.

.. code-block:: pycon

    >>> def fix_nan(x):
    ...     if x != x:  # only true for NaN
    ...         return float('-inf')
    ...     else:
    ...         return x
    ...

Let's check out :ref:`TL;DR 2 <tldr2>` to see how this can be
incorporated into the simple key function from :ref:`TL;DR 1 <tldr1>`.

.. _tldr2:

TL;DR 2 - Handling Crappy, Real-World Input
+++++++++++++++++++++++++++++++++++++++++++

Let's see how our elegant key function from :ref:`TL;DR 1 <tldr1>` has
become bastardized in order to support handling mixed real-world data
and user customizations.

.. code-block:: pycon

    >>> def natsort_key(x, as_float=False, signed=False, as_path=False):
    ...     if as_float:
    ...         regex = signed_float if signed else unsigned_float
    ...     else:
    ...         regex = signed_int if signed else unsigned_int
    ...     try:
    ...         if as_path:
    ...             x = decompose_path_into_components(x)  # Decomposes into list of strings
    ...         # If this raises a TypeError, input is not a string.
    ...         split_input = re.split(regex, x)
    ...     except TypeError:
    ...         try:
    ...             # Does this need to be applied recursively (list-of-list)?
    ...             return tuple(map(natsort_key, x))
    ...         except TypeError:
    ...             # Must be a number
    ...             ret = ('', fix_nan(x))  # Maintain string-number-string pattern
    ...             return (ret,) if as_path else ret  # as_path returns tuple-of-tuples
    ...     else:
    ...         split_input = filter(None, split_input)  # removes null strings
    ...         # Note that the coerce_to_int/coerce_to_float functions
    ...         # are also modified to use the fix_nan function.
    ...         if as_float:
    ...             coerced_input = (coerce_to_float(s) for s in split_input)
    ...         else:
    ...             coerced_input = (coerce_to_int(s) for s in split_input)
    ...         return tuple(sep_inserter(coerced_input, ''))
    ...

And this doesn't even show handling :class:`bytes` type! Notice that we have
to do non-obvious things like modify the return form of numbers when ``as_path``
is given, just to avoid comparing strings and numbers for the case in which a
user provides input like ``['/home/me', 42]``.

Let's take it out for a spin!

.. code-block:: pycon

    >>> danger = [7, float('nan'), 22.7, '19', '-14', '59.123', 4]
    >>> sorted(danger, key=lambda x: natsort_key(x, as_float=True, signed=True))
    [nan, '-14', 4, 7, '19', 22.7, '59.123']
    >>>
    >>> paths = ['Folder (1)/file.tar.gz',
    ...          'Folder/file.tar.gz',
    ...          123456]
    >>> sorted(paths, key=lambda x: natsort_key(x, as_path=True))
    [123456, 'Folder/file.tar.gz', 'Folder (1)/file.tar.gz']

Here Be Dragons: Adding Locale Support
--------------------------------------

.. contents::
    :local:

Probably the most challenging special case I had to handle was getting
:mod:`natsort` to handle sorting the non-numerical parts of input
correctly, and also allowing it to sort the numerical bits in different
locales. This was in no way what I originally set out to do with this
library, so I was
`caught a bit off guard when the request was initially made`_.
I discovered the :mod:`locale` library, and assumed that if it's part of
Python's StdLib there can't be too many dragons, right?

.. admonition:: INCOMPLETE LIST OF DRAGONS

    - https://github.com/SethMMorton/natsort/issues/21
    - https://github.com/SethMMorton/natsort/issues/22
    - https://github.com/SethMMorton/natsort/issues/23
    - https://github.com/SethMMorton/natsort/issues/36
    - https://github.com/SethMMorton/natsort/issues/44
    - https://bugs.python.org/issue2481
    - https://bugs.python.org/issue23195
    - https://stackoverflow.com/questions/3412933/python-not-sorting-unicode-properly-strcoll-doesnt-help
    - https://stackoverflow.com/questions/22203550/sort-dictionary-by-key-using-locale-collation
    - https://stackoverflow.com/questions/33459384/unicode-character-not-in-range-when-calling-locale-strxfrm
    - https://stackoverflow.com/questions/36431810/sort-numeric-lines-with-thousand-separators
    - https://stackoverflow.com/questions/45734562/how-can-i-get-a-reasonable-string-sorting-with-python

These can be summed up as follows:

#. :mod:`locale` is a thin wrapper over your operating system's *locale*
   library, so if *that* is broken (like it is on BSD and OSX) then
   :mod:`locale` is broken in Python.
#. Because of a bug in legacy Python (i.e. Python 2), there is no uniform
   way to use the :mod:`locale` sorting functionality between legacy Python
   and Python 3.
#. People have differing opinions of how capitalization should affect word
   order.
#. There is no built-in way to handle locale-dependent thousands separators
   and decimal points *robustly*.
#. Proper handling of Unicode is complicated.
#. Proper handling of :mod:`locale` is complicated.

Easily over half of the code in :mod:`natsort` is in some way dealing with some
aspect of :mod:`locale` or basic case handling. It would have been impossible
to get right without a `really good`_ `testing strategy`_.

Don't expect any more TL;DR's... if you want to see how all this is fully
incorporated into the :mod:`natsort` algorithm then please take a look
`at the code`_.  However, I will hint at how specific steps are taken in
each section.

Let's see how we can handle some of the dragons, one-by-one.

Basic Case Control Support
++++++++++++++++++++++++++

Without even thinking about the mess that is adding :mod:`locale` support,
:mod:`natsort` can introduce support for controlling how case is interpreted.

First, let's take a look at how it is sorted by default (due to
where characters lie on the `ASCII table`_).

.. code-block:: pycon

    >>> a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    >>> sorted(a)
    ['Apple', 'Banana', 'Corn', 'apple', 'banana', 'corn']

All uppercase letters come before lowercase letters in the `ASCII table`_,
so all capitalized words appear first. Not everyone agrees that this
is the correct order. Some believe that the capitalized words should
be last (``['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']``).
Some believe that both the lowercase and uppercase versions
should appear together
(``['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']``).
Some believe that both should be true ☹. Some people don't care at all [#f3]_.

Solving the first case (I call it *LOWERCASEFIRST*) is actually pretty
easy... just call the :meth:`str.swapcase` method on the input.

.. code-block:: pycon

    >>> sorted(a, key=lambda x: x.swapcase())
    ['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']

The last (i call it *IGNORECASE*) should be super easy, right?
Simply call :meth:`str.lowercase` on the input. This will work but may
not always give the correct answer on non-latin character sets. It's
a good thing that in Python 3.3
:meth:`str.casefold` was introduced, which does a better job of removing
all case information from unicode characters in
non-latin alphabets.

.. code-block:: pycon

    >>> def remove_case(x):
    ...     try:
    ...         return x.casefold()
    ...     except AttributeError:  # Legacy Python backwards compatibility
    ...         return x.lowercase()
    ...
    >>> sorted(a, key=remove_case)
    ['Apple', 'apple', 'Banana', 'banana', 'corn', 'Corn']

The middle case (I call it *GROUPLETTERS*) is less straightforward.
The most efficient way to handle this is to duplicate each character
with its lowercase version and then the original character.

.. code-block:: pycon

    >>> import itertools
    >>> def groupletters(x):
    ...     return ''.join(itertools.chain.from_iterable((remove_case(y), y) for y in x))
    ...
    >>> groupletters('Apple')
    'aAppppllee'
    >>> groupletters('apple')
    'aappppllee'
    >>> sorted(a, key=groupletters)
    ['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']

The effect of this is that both ``'Apple'`` and ``'apple'`` are
placed adjacent to each other because their transformations both begin
with ``'a'``, and then the second character can be used to order them
appropriately with respect to each other.

There's a problem with this, though. Within the context of :mod:`natsort`
we are trying to correctly sort numbers and those should be left alone.

.. code-block:: pycon

    >>> a = ['Apple5', 'apple', 'Apple4E10', 'Banana']
    >>> sorted(a, key=lambda x: natsort_key(x, as_float=True))
    ['Apple5', 'Apple4E10', 'Banana', 'apple']
    >>> sorted(a, key=lambda x: natsort_key(groupletters(x), as_float=True))
    ['Apple4E10', 'Apple5', 'apple', 'Banana']
    >>> groupletters('Apple4E10')
    'aAppppllee44eE1100'

We messed up the numbers! Looks like :func:`groupletters` needs to be applied
*after* the strings are broken into their components. I'm not going to show
how this is done here, but basically it requires applying the function in
the ``else:`` block of :func:`coerce_to_int`/:func:`coerce_to_float`.

.. code-block:: pycon

    >>> better_groupletters = natsort_keygen(alg=ns.GROUPLETTERS | ns.REAL)
    >>> better_groupletters('Apple4E10')
    ('aAppppllee', 40000000000.0)
    >>> sorted(a, key=better_groupletters)
    ['Apple5', 'Apple4E10', 'apple', 'Banana']

Of course, applying both *LOWERCASEFIRST* and *GROUPLETTERS* is just
a matter of turning on both functions.

Basic Unicode Support
+++++++++++++++++++++

Unicode is hard and complicated. Here's an example.

.. code-block:: pycon

    >>> b = [b'\x66', b'\x65', b'\xc3\xa9', b'\x65\xcc\x81', b'\x61', b'\x7a']
    >>> a = [x.decode('utf8') for x in b]
    >>> a  # doctest: +SKIP
    ['f', 'e', 'é', 'é', 'a', 'z']
    >>> sorted(a)  # doctest: +SKIP
    ['a', 'e', 'é', 'f', 'z', 'é']

There are more than one way to represent the character 'é' in Unicode.
In fact, many characters have multiple representations. This is a challenge
because comparing the two representations would return ``False`` even though
they *look* the same.

.. code-block:: pycon

    >>> a[2] == a[3]
    False

Alas, since characters are compared based on the numerical value of their
representation, sorting Unicode often gives unexpected results (like seeing
'é' come both *before* and *after* 'z').

The original approach that :mod:`natsort` took with respect to non-ASCII
Unicode characters was to say "just use
the :mod:`locale` or :mod:`PyICU` library" and then cross it's fingers
and hope those libraries take care of it. As you will find in the following
sections, that comes with its own baggage, and turned out to not always work
anyway (see https://stackoverflow.com/q/45734562/1399279). A more robust
approach is to handle the Unicode out-of-the-box without invoking a
heavy-handed library like :mod:`locale` or :mod:`PyICU`.
To do this, we must use *normalization*.

To fully understand Unicode normalization,
`check out some official Unicode documentation`_.
Just kidding... that's too much text. The following StackOverflow answers do
a good job at explaining Unicode normalization in simple terms:
https://stackoverflow.com/a/7934397/1399279 and
https://stackoverflow.com/a/7931547/1399279. Put simply, normalization
ensures that Unicode characters with multiple representations are in
some canonical and consistent representation so that (for example) comparisons
of the characters can be performed in a sane way. The following discussion
assumes you at least read the StackOverflow answers.

Looking back at our 'é' example, we can see that the two versions were
constructed with the byte strings ``b'\xc3\xa9'`` and ``b'\x65\xcc\x81'``.
The former representation is actually
`LATIN SMALL LETTER E WITH ACUTE <https://www.fileformat.info/info/unicode/char/e9/index.htm>`_
and is a single character in the Unicode standard. This is known as the
*compressed form* and corresponds to the 'NFC' normalization scheme.
The latter representation is actually the letter 'e' followed by
`COMBINING ACUTE ACCENT <https://www.fileformat.info/info/unicode/char/0301/index.htm>`_
and so is two characters in the Unicode standard. This is known as the
*decompressed form* and corresponds to the 'NFD' normalization scheme.
Since the first character in the decompressed form is actually the letter 'e',
when compared to other ASCII characters it fits where you might expect.
Unfortunately, all Unicode compressed form characters come after the
ASCII characters and so they always will be placed after 'z' when sorting.

It seems that most Unicode data is stored and shared in the compressed form
which makes it challenging to sort. This can be solved by normalizing all
incoming Unicode data to the decompressed form ('NFD') and *then* sorting.

.. code-block:: pycon

    >>> import unicodedata
    >>> c = [unicodedata.normalize('NFD', x) for x in a]
    >>> c  # doctest: +SKIP
    ['f', 'e', 'é', 'é', 'a', 'z']
    >>> sorted(c)  # doctest: +SKIP
    ['a', 'e', 'é', 'é', 'f', 'z']

Huzzah! Sane sorting without having to resort to :mod:`locale`!

Using Locale to Compare Strings
+++++++++++++++++++++++++++++++

The :mod:`locale` module is actually pretty cool, and provides lowly
spare-time programmers like myself a way to handle the daunting task
of proper locale-dependent support of their libraries and utilities.
Having said that, it can be a bit of a bear to get right,
`although they do point out in the documentation that it will be painful to use`_.
Aside from the caveats spelled out in that link, it turns out that just
comparing strings with :mod:`locale` in a cross-platform and
cross-python-version manner is not as straightforward as one might hope.

First, how to use :mod:`locale` to compare strings? It's actually
pretty straightforward. Simply run the input through the :mod:`locale`
transformation function :func:`locale.strxfrm`.

.. code-block:: pycon

    >>> import locale, sys
    >>> locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    'en_US.UTF-8'
    >>> a = ['a', 'b', 'ä']
    >>> sorted(a)
    ['a', 'b', 'ä']
    >>> # The below fails on OSX, so don't run doctest on darwin.
    >>> is_osx = sys.platform == 'darwin'
    >>> sorted(a, key=locale.strxfrm) if not is_osx else ['a', 'ä', 'b']
    ['a', 'ä', 'b']
    >>>
    >>> a = ['apple', 'Banana', 'banana', 'Apple']
    >>> sorted(a, key=locale.strxfrm) if not is_osx else ['apple', 'Apple', 'banana', 'Banana']
    ['apple', 'Apple', 'banana', 'Banana']

It turns out that locale-aware sorting groups numbers in the same
way as turning on *GROUPLETTERS* and *LOWERCASEFIRST*.
The trick is that you have to apply :func:`locale.strxfrm` only to non-numeric
characters; otherwise, numbers won't be parsed properly. Therefore, it must
be applied as part of the :func:`coerce_to_int`/:func:`coerce_to_float`
functions in a manner similar to :func:`groupletters`.

As you might have guessed, there is a small problem.
It turns out the there is a bug in the legacy Python implementation of
:func:`locale.strxfrm` that causes it to outright fail for :func:`unicode`
input (https://bugs.python.org/issue2481). :func:`locale.strcoll` works,
but is intended for use with ``cmp``, which does not exist in current Python
implementations. Luckily, the :func:`functools.cmp_to_key` function
makes :func:`locale.strcoll` behave like :func:`locale.strxfrm`.

Handling Broken Locale On OSX
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

But what if the underlying *locale* implementation that :mod:`locale`
relies upon is simply broken? It turns out that the *locale* library on
OSX (and other BSD systems) is broken (and for some reason has never been
fixed?), and so :mod:`locale` does not work as expected.

How do I define doesn't work as expected?

.. code-block:: pycon

    >>> a = ['apple', 'Banana', 'banana', 'Apple']
    >>> sorted(a)
    ['Apple', 'Banana', 'apple', 'banana']
    >>>
    >>> sorted(a, key=locale.strxfrm) if is_osx else sorted(a)
    ['Apple', 'Banana', 'apple', 'banana']

IT'S SORTING AS IF :func:`locale.stfxfrm` WAS NEVER USED!! (and it's worse
once non-ASCII characters get thrown into the mix.) I'm really not
sure why this is considered OK for the OSX/BSD maintainers to not fix,
but it's more than frustrating for poor developers who have been dragged
into the *locale* game kicking and screaming. *<deep breath>*.

So, how to deal with this situation? There are two ways to do so.

#.  Detect if :mod:`locale` is sorting incorrectly (i.e. ``dumb``) by seeing
    if ``'A'`` is sorted before ``'a'`` (incorrect) or not.

    .. code-block:: pycon

        >>> # This is genuinely the name of this function.
        >>> # See natsort.compat.locale.py
        >>> def dumb_sort():
        ...     return locale.strxfrm('A') < locale.strxfrm('a')
        ...

    If a ``dumb`` *locale* implementation is found, then automatically
    turn on *LOWERCASEFIRST* and *GROUPLETTERS*.
#.  Use an alternate library if installed. `ICU <http://site.icu-project.org/>`_
    is a great and powerful library that has a pretty decent Python port
    called (you guessed it) `PyICU <https://pypi.org/project/PyICU/>`_.
    If a user has this library installed on their computer, :mod:`natsort`
    chooses to use that instead of :mod:`locale`. With a little bit of
    planning, one can write a set of wrapper functions that call
    the correct library under the hood such that the business logic never
    has to know what library is being used (see `natsort.compat.locale.py`_).

Let me tell you, this little complication really makes a challenge of testing
the code, since one must set up different environments on different operating
systems in order to test all possible code paths. Not to mention that
certain checks *will* fail for certain operating systems and environments
so one must be diligent in either writing the tests not to fail, or ignoring
those tests when on offending environments.

Handling Locale-Aware Numbers
+++++++++++++++++++++++++++++

`Thousands separator support`_ is a problem that I knew would someday be
requested but had decided to push off until a rainy day. One day it finally
rained, and I decided to tackle the problem.

So what is the problem? Consider the number ``1,234,567`` (assuming the
``','`` is the thousands separator). Try to run that through :func:`int`
and you will get a :exc:`ValueError`. To handle this properly the thousands
separators must be removed.

.. code-block:: pycon

    >>> float('1,234,567'.replace(',', ''))
    1234567.0

What if, in our current locale, the thousands separator is ``'.'`` and
the ``','`` is the decimal separator (like for the German locale *de_DE*)?

.. code-block:: pycon

    >>> float('1.234.567'.replace('.', '').replace(',', '.'))
    1234567.0
    >>> float('1.234.567,89'.replace('.', '').replace(',', '.'))
    1234567.89

This is pretty much what :func:`locale.atoi` and :func:`locale.atof` do
under the hood. So what's the problem? Why doesn't :mod:`natsort` just
use this method under its hood?
Well, let's take a look at what would happen if we send some possible
:mod:`natsort` input through our the above function:

.. code-block:: pycon

    >>> natsort_key('1,234 apples, please.'.replace(',', ''))
    ('', 1234, ' apples please.')
    >>> natsort_key('Sir, €1.234,50 please.'.replace('.', '').replace(',', '.'), as_float=True)
    ('Sir. €', 1234.5, ' please')

Any character matching the thousands separator was dropped, and anything
matching the decimal separator was changed to ``'.'``! If these characters
were critical to how your data was ordered, this would break :mod:`natsort`.

The first solution one might consider would be to first decompose the
input into sub-components (like we did for the *GROUPLETTERS* method
above) and then only apply these transformations on the number components.
This is a chicken-and-egg problem, though, because *we cannot appropriately
separate out the numbers because of the thousands separators and
non-'.' decimal separators* (well, at least not without making multiple
passes over the data which I do not consider to be a valid option).

Regular expressions to the rescue! With regular expressions, we can
remove the thousands separators and change the decimal separator only
when they are actually within a number. Once the input has been
pre-processed with this regular expression, all the infrastructure
shown previously will work.

Beware, these regular expressions will make your eyes bleed.

.. code-block:: pycon

    >>> decimal = ','  # Assume German locale, so decimal separator is ','
    >>> # Look-behind assertions cannot accept range modifiers, so instead of i.e.
    >>> # (?<!\.[0-9]{1,3}) I have to repeat the look-behind for 1, 2, and 3.
    >>> nodecimal = r'(?<!{dec}[0-9])(?<!{dec}[0-9]{{2}})(?<!{dec}[0-9]{{3}})'.format(dec=decimal)
    >>> strip_thousands = r'''
    ...     (?<=[0-9]{{1}})  # At least 1 number
    ...     (?<![0-9]{{4}})  # No more than 3 numbers
    ...     {nodecimal}      # Cannot follow decimal
    ...     {thou}           # The thousands separator
    ...     (?=[0-9]{{3}}    # Three numbers must follow
    ...      ([^0-9]|$)      # But a non-number after that
    ...     )
    ... '''.format(nodecimal=nodecimal, thou=re.escape('.'))  # Thousands separator is '.' in German locale.
    ...
    >>> re.sub(strip_thousands, '', 'Sir, €1.234,50 please.', flags=re.X)
    'Sir, €1234,50 please.'
    >>>
    >>> # The decimal point must be preceded by a number or after
    >>> # a number. This option only needs to be performed in the
    >>> # case when the decimal separator for the locale is not '.'.
    >>> switch_decimal = r'(?<=[0-9]){decimal}|{decimal}(?=[0-9])'
    >>> switch_decimal = switch_decimal.format(decimal=decimal)
    >>> re.sub(switch_decimal, '.', 'Sir, €1234,50 please.', flags=re.X)
    'Sir, €1234.50 please.'
    >>>
    >>> natsort_key('Sir, €1234.50 please.', as_float=True)
    ('Sir, €', 1234.5, ' please.')

Final Thoughts
--------------

My hope is that users of :mod:`natsort` never have to think about or worry
about all the bookkeeping or any of the details described above, and that using
:mod:`natsort` seems to magically "just work". For those of you who
took the time to read this engineering description, I hope it has enlightened
you to some of the issues that can be encountered when code is released
into the wild and has to accept "real-world data", or to what happens
to developers who naïvely make bold assumptions that are counter to
what the rest of the world assumes.

.. rubric:: Footnotes

.. [#f1]
    *"But if you hadn't removed the leading empty string from re.split this
    wouldn't have happened!!"* I can hear you saying. Well, that's true. I don't
    have a *great* reason for having done that except that in an earlier
    non-optimal incarnation of the algorithm I needed to it, and it kind of
    stuck, and it made other parts of the code easier if the assumption that
    there were no empty strings was valid.
.. [#f2]
    I'm not going to show how this is implemented in this document,
    but if you are interested you can look at the code to
    :func:`sep_inserter` in `util.py`_.
.. [#f3]
    Handling each of these is straightforward, but coupled with the rapidly
    fracturing execution paths presented in :ref:`TL;DR 2 <tldr2>` one can
    imagine this will get out of hand quickly. If you take a look at
    `natsort.py`_ and `util.py`_ you can observe that to avoid this I take
    a more functional approach to construting the :mod:`natsort` algorithm
    as opposed to the procedural approach illustrated in
    :ref:`TL;DR 1 <tldr1>` and :ref:`TL;DR 2 <tldr2>`.

.. _ASCII table: https://www.asciitable.com/
.. _getting sorting right is surprisingly hard: http://www.compciv.org/guides/python/fundamentals/sorting-collections-with-sorted/
.. _This astonished: https://github.com/SethMMorton/natsort/issues/19
.. _a lot: https://stackoverflow.com/questions/29548742/python-natsort-sort-strings-recursively
.. _of people: https://stackoverflow.com/questions/24045348/sort-set-of-numbers-in-the-form-xx-yy-in-python
.. _and some people aren't very nice when they are astonished:
    https://github.com/xolox/python-naturalsort/blob/ed3e6b6ffaca3bdea3b76e08acbb8bd2a5fee463/README.rst#why-another-natsort-module
.. _fastnumbers: https://github.com/SethMMorton/fastnumbers
.. _as part of my testing: https://github.com/SethMMorton/natsort/blob/master/test_natsort/slow_splitters.py
.. _this one for coercion: https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python
.. _this one for checking: https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
.. _most natural sort solutions for python on Stack Overflow: https://stackoverflow.com/q/4836710/1399279
.. _80%/20%: https://en.wikipedia.org/wiki/Pareto_principle
.. _The first major special case I encountered was sorting filesystem paths: https://github.com/SethMMorton/natsort/issues/3
.. _The second major special case I encountered was sorting of different types: https://github.com/SethMMorton/natsort/issues/7
.. _A rather unexpected special case I encountered was sorting collections containing NaN:
   https://github.com/SethMMorton/natsort/issues/27
.. _It's hard to compare floating point numbers: http://www.drdobbs.com/cpp/its-hard-to-compare-floating-point-numbe/240149806
.. _caught a bit off guard when the request was initially made: https://github.com/SethMMorton/natsort/issues/14
.. _at the code: https://github.com/SethMMorton/natsort/tree/master/natsort
.. _natsort.py: https://github.com/SethMMorton/natsort/blob/master/natsort/natsort.py
.. _util.py: https://github.com/SethMMorton/natsort/blob/master/natsort/util.py
.. _although they do point out in the documentation that it will be painful to use:
   https://docs.python.org/3/library/locale.html#background-details-hints-tips-and-caveats
.. _natsort.compat.locale.py: https://github.com/SethMMorton/natsort/blob/master/natsort/compat/locale.py
.. _Thousands separator support: https://github.com/SethMMorton/natsort/issues/36
.. _really good: https://hypothesis.readthedocs.io/en/latest/
.. _testing strategy: https://docs.pytest.org/en/latest/
.. _check out some official Unicode documentation: https://unicode.org/reports/tr15/
