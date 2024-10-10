# Contributing

If you have an idea for how to improve `natsort`, please contribute! It can
be as simple as a bug fix or documentation update, or as complicated as a more
robust algorithm. Contributions that change the public API of
`natsort` will have to ensure that the library does not become
less usable after the contribution and is backwards-compatible (unless there is
a good reason not to be).

Located in the `dev/` folder is development collateral such as formatting and
patching scripts. The only development collateral not in the `dev/`
folder are those files that are expected to exist in the the top-level directory
(such as `pyproject.toml`, `tox.ini`, and CI configuration). All of these scripts
can either be run with the python stdandard library, or have hooks in `tox`.

I do not have strong opinions on how one should contribute, so
I have copy/pasted some text verbatim from the
[Contributor's Guide](http://docs.python-requests.org/en/latest/dev/contributing/) section of
the [requests](https://github.com/kennethreitz/requests) library in
lieu of coming up with my own.

> ### Steps for Submitting Code

> When contributing code, you'll want to follow this checklist:

> - Fork the repository on GitHub.
> -  Run the tests to confirm they all pass on your system.
     If they don't, you'll need to investigate why they fail.
     If you're unable to diagnose this yourself,
     raise it as a bug report.
> - Write tests that demonstrate your bug or feature. Ensure that they fail.
> - Make your change.
> - Run the entire test suite again, confirming that all tests pass including the
    ones you just added.
> - Send a GitHub Pull Request to the main repository's main branch.
    GitHub Pull Requests are the expected method of code collaboration on this project.

> ### Documentation Contributions
> Documentation improvements are always welcome! The documentation files live in the
  docs/ directory of the codebase. They're written in
  [reStructuredText](http://docutils.sourceforge.net/rst.html), and use
  [Sphinx](http://sphinx-doc.org/index.html)
  to generate the full suite of documentation.

> When contributing documentation, please do your best to follow the style of the
  documentation files. This means a soft-limit of 79 characters wide in your text
  files and a semi-formal, yet friendly and approachable, prose style.
