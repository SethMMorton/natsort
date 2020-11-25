#! /usr/bin/env python

"""
Cross-platform bump of version with special CHANGELOG modification.
INTENDED TO BE CALLED FROM PROJECT ROOT, NOT FROM dev/!
"""

import subprocess
import sys

try:
    bump_type = sys.argv[1]
except IndexError:
    sys.exit("Must pass 'bump_type' argument!")
else:
    if bump_type not in ("major", "minor", "patch"):
        sys.exit('bump_type must be one of "major", "minor", or "patch"!')


def git(cmd, *args):
    """Wrapper for calling git"""
    try:
        subprocess.run(["git", cmd, *args], check=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Call to git failed!", file=sys.stderr)
        print("STDOUT:", e.stdout, file=sys.stderr)
        print("STDERR:", e.stderr, file=sys.stderr)
        sys.exit(e.returncode)


def bumpversion(severity, *args, catch=False):
    """Wrapper for calling bumpversion"""
    cmd = ["bump2version", *args, severity]
    try:
        if catch:
            return subprocess.run(
                cmd, check=True, capture_output=True, text=True
            ).stdout
        else:
            subprocess.run(cmd, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Call to bump2version failed!", file=sys.stderr)
        print("STDOUT:", e.stdout, file=sys.stderr)
        print("STDERR:", e.stderr, file=sys.stderr)
        sys.exit(e.returncode)


# Do a dry run of the bump to find what the current version is and what it will become.
data = bumpversion(bump_type, "--dry-run", "--list", catch=True)
data = dict(x.split("=") for x in data.splitlines())

# Execute the bumpversion.
bumpversion(bump_type)

# Post-process the changelog with things that bumpversion is not good at updating.
with open("CHANGELOG.md") as fl:
    changelog = fl.read().replace(
        "<!---Comparison links-->",
        "<!---Comparison links-->\n[{new}]: {url}/{current}...{new}".format(
            new=data["new_version"],
            current=data["current_version"],
            url="https://github.com/SethMMorton/natsort/compare",
        ),
    )
with open("CHANGELOG.md", "w") as fl:
    fl.write(changelog)

# Finally, add the CHANGELOG.md changes to the previous commit.
git("add", "CHANGELOG.md")
git("commit", "--amend", "--no-edit")
git("tag", "--force", data["new_version"], "HEAD")
