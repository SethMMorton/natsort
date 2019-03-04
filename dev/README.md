# Development Collateral

This file contains some files useful for development.

- `bump.sh` - Execute `bumpversion` then post-processes the CHANGELOG to handle corner-cases
  that `bumpversion` cannot. Requires [`bump2version`](https://github.com/c4urself/bump2version),
  which is the maintained fork of [`bumpversion`](https://github.com/peritus/bumpversion).
- `clean.sh` - This file cleans most files that are created during development.
  Run in the project home directory.
- `requirements.txt` - Requirements to run tests.
