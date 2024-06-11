#!/bin/bash

# Helper script to release the Python SDK

set -e

# Read the contents of the files into variables
version=$(<src/onepassword/version)
build=$(<src/onepassword/version-build)
changelog=$(<src/onepassword/changelogs/"${version}"-"${build}")

# Check if Github CLI is installed
if ! command -v gh &> /dev/null; then
	echo "gh is not installed";\
	exit 1;\
fi

git tag -a -s  "v${version}" -m "${version}"

# Get Current Branch Name
branch="$(git rev-parse --abbrev-ref HEAD)"

# if on main, then stash changes and create RC branch
if [[ "${branch}" = "main" ]]; then
    git stash
    git fetch origin
    git checkout -b rc/"${version}"
    git stash pop
fi

# Add changes and commit/push to branch
git add .
git commit -m "Release for ${version}"
git push origin ${branch}

# Ensure GITHUB_TOKEN env var is set
if [ -z "${GITHUB_TOKEN}" ]; then
  echo "GITHUB_TOKEN environment variable is not set."
  exit 1
fi

gh release create "${version}" --title "Release ${version}" --notes "${changelog}" --repo github.com/1Password/onepassword-sdk-python
