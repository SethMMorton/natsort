#! /bin/sh

set -eux

# Determine what the new version will be
new_version=$(bump2version --dry-run --list "${1}" | grep "^new_version" | sed -r s,"^.*=",,)
current_version=$(bump2version --dry-run --list "${1}" | grep "^current_version" | sed -r s,"^.*=",,)

# Perform the bumpversion, then perform the post-processing on the CHANGELOG.md
# to update the version comparison list.
bump2version "${1}"
URL="https://github.com/SethMMorton/natsort/compare"
sed -E "s|(<!---Comparison links-->)|\1\n[${new_version}]: ${URL}/${current_version}...${new_version}|" -i.bak CHANGELOG.md
rm CHANGELOG.md.bak  # Remove backup created by in-place sed

# Commit the change just made and then move the tag
git add CHANGELOG.md
git commit --amend --no-edit
git tag --force "${new_version}" HEAD
