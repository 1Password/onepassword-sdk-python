#!/bin/bash
# Helper script to prepare a Python Release for the SDKs.

set -e

enforce_latest_code() {
    if [[ -n "$(git status --porcelain=v1)" ]]; then
        echo "ERROR: working directory is not clean."
        echo "Please stash your changes and try again."
        exit 1
    fi

    git fetch --quiet origin main
    if [[ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]]; then
        echo "ERROR: This script was not run from the latest code from origin/main."
        echo "Make sure to update your git branch with the latest from main and try again."
        exit 1
    fi
}

# Enforce that the working directory is clean and run off the latest version of origin/main.
enforce_latest_code

# Make sure origin/main is up-to-date
if ! git fetch origin main; then
  echo "Cannot update from origin. Abort." >&2
  exit 1
fi


if ! test -e "$SDK_BUILD_FILE"; then
  echo "Cannot locate build file. Stopping." >&2
  exit 1
fi

# Swap the version numbers with the updated ones
make version_swap

# Stash changes
git stash 

# Create and checkout release branch with new version
git fetch origin
git checkout origin/main
git status
git checkout -b "${SDK_NAME}-rc/${SDK_VERSION}"

# Restore version changes
git stash pop

# Push changes
git push origin "${SDK_NAME}-rc/${SDK_VERSION}"
