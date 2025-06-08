#! /usr/bin/env python3

"""
Bump version of natsort.

Cross-platform bump of version with special CHANGELOG modification.
INTENDED TO BE CALLED FROM PROJECT ROOT, NOT FROM dev/!
"""

from __future__ import annotations

import datetime
import pathlib
import subprocess
import sys

from setuptools_scm import get_version

# Ensure a clean repo before moving on.
ret = subprocess.run(
    ["git", "status", "--porcelain", "--untracked-files=no"],
    check=True,
    capture_output=True,
    text=True,
)
if ret.stdout:
    sys.exit("Cannot bump unless the git repo has no changes.")


# A valid bump must have been given.
try:
    bump_type = sys.argv[1]
except IndexError:
    sys.exit("Must pass 'bump_type' argument!")
else:
    if bump_type not in ("major", "minor", "patch"):
        sys.exit('bump_type must be one of "major", "minor", or "patch"!')


def git(cmd: str, *args: str) -> None:
    """Call git."""
    try:
        subprocess.run(["git", cmd, *args], check=True, text=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


# Use setuptools-scm to identify the current version
current_version = get_version(
    root="..",
    relative_to=__file__,
    local_scheme="no-local-version",
    version_scheme="only-version",
)

# Increment the version according to the bump type
version_components = list(map(int, current_version.split(".")))
incr_index = {"major": 0, "minor": 1, "patch": 2}[bump_type]
version_components[incr_index] += 1
for i in range(incr_index + 1, 3):
    version_components[i] = 0
next_version = ".".join(map(str, version_components))

# Update the changelog.
changelog = pathlib.Path("CHANGELOG.md").read_text()

# Add a date to this entry.
changelog = changelog.replace(
    "Unreleased",
    f"Unreleased\n---\n\n[{next_version}] - {datetime.datetime.now():%Y-%m-%d}",
)

# Add links to the entries.
changelog = changelog.replace(
    "<!---Comparison links-->",
    "<!---Comparison links-->\n[{new}]: {url}/{current}...{new}".format(
        new=next_version,
        current=current_version,
        url="https://github.com/SethMMorton/natsort/compare",
    ),
)

# Write the changelog
pathlib.Path("CHANGELOG.md").write_text(changelog)

# Add the CHANGELOG.md changes and commit & tag.
git("add", "CHANGELOG.md")
git("commit", "--message", f"Bump version: {current_version} → {next_version}")
git("tag", next_version, "HEAD")
