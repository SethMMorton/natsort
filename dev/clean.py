#! /usr/bin/env python

"""
Cross-platform clean of working directory.
INTENDED TO BE CALLED FROM PROJECT ROOT, NOT FROM dev/!
"""

import pathlib
import shutil

# Directories to obliterate
dirs = [
    pathlib.Path("build"),
    pathlib.Path("dist"),
    pathlib.Path(".pytest_cache"),
    pathlib.Path(".hypothesis"),
    pathlib.Path(".tox"),
]
dirs += pathlib.Path.cwd().glob("*.egg-info")
for d in dirs:
    if d.is_dir():
        shutil.rmtree(d, ignore_errors=True)
    elif d.is_file():
        d.unlink()  # just in case there is a file.

# Clean up any stray __pycache__.
for d in pathlib.Path.cwd().rglob("__pycache__"):
    shutil.rmtree(d, ignore_errors=True)

# Shouldn't be any .pyc left, but just in case
for f in pathlib.Path.cwd().rglob("*.pyc"):
    f.unlink()
