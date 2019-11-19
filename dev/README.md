# Development Collateral

This file contains some files useful for development.

- `bump.py` - Execute `bumpversion` then post-processes the CHANGELOG to handle corner-cases
  that `bumpversion` cannot. Requires [`bump2version`](https://github.com/c4urself/bump2version),
  which is the maintained fork of [`bumpversion`](https://github.com/peritus/bumpversion).
  It is not really intended to be called directly, but instead through `tox -e bump`.
- `clean.py` - This file cleans most files that are created during development.
  Run in the project home directory.
  It is not really intended to be called directly, but instead through `tox -e clean`.
- `requirements.in` - Our direct requirements to run tests.
- `requirements.txt` - All pinned requirements to run tests.
