#!/bin/bash

# Helper script to push the SDK release after review. 

RC_BRANCH="${SDK_NAME}-rc/${SDK_VERSION}"

enforce_latest_code() {
    if [[ -n "$(git status --porcelain=v1)" ]]; then
        echo "ERROR: working directory is not clean."
        echo "Please stash your changes and try again."
        exit 1
    fi

    git fetch --quiet origin "$RC_BRANCH"
    if [[ "$(git rev-parse HEAD)" != "$(git rev-parse "origin/$RC_BRANCH")" ]]; then
        echo "ERROR: This script was not run from the latest code from this RC branch."
        echo "Make sure to update your git branch with the latest commits and try again."
        exit 1
    fi
}

# Enforce that the working directory is clean and run off the latest version of origin/main.
# enforce_latest_code

git pull origin "${RC_BRANCH}"

# Creating and pushing the tag for the release candidate 
git tag -a "$SDK_VERSION" -m "$SDK_VERSION"
git push --tags origin "${RC_BRANCH}"

gh release create "${SDK_VERSION}" --title "Release ${SDK_VERSION}" --notes "${RELEASE_NOTES}"
