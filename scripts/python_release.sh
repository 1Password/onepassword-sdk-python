#!/bin/bash

# Helper script to prepare a Python Release for the SDKs.

set -e

# Read the version number and build number from the respective files
version_number=$(< src/onepassword/version.txt)
build_number=$(< src/onepassword/version-build.txt)
# Function to validate the version number format x.y.z(-beta.w)
validate_version_number() {
    local version="$1"
    if [[ "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-beta\.[0-9]+)?$ ]]; then
        echo "Updated version number is: ${version}"
        return 0
    else
        echo "Invalid version number format: ${version}"
        return 1
    fi
}

# Function to validate the build number format Mmmppbb
validate_build_number() {
    local build="$1"
    if [[ "${build}" =~ ^[0-9]{1}[0-9]{2}[0-9]{2}[0-9]{2}$ ]]; then
        echo "Updated build number is: ${build}"
        return 0
    else
        echo "Invalid build number format: ${build}"
        return 1
    fi
}

# Validate the version number and build number from their respective files
if ! validate_version_number "$version_number" || ! validate_build_number "$build_number"; then
    exit 1
fi

# Prompt the user to input multiline text
echo "Enter your multiline text (press Ctrl+D when finished):"
changelog_content=""

# Read multiline input from the user until Ctrl+D is pressed
while IFS= read -r line; do
    changelog_content+="${line}"$'\n' # Append each line to the variable with a newline character
done

git tag -a -s  "v${version_number}" -m "${version_number}"

# Get Current Branch Name
branch="$(git rev-parse --abbrev-ref HEAD)"

# if on main, then stash changes and create RC branch
if [[ "${branch}" = "main" ]]; then
    git stash
    git fetch origin
    git checkout -b rc/"${version_number}"
    git stash pop
fi

# Add changes and commit/push to branch
git add .
git commit -m "Release for ${version_number}"
git push origin ${branch}

# Login with Github CLI
gh auth login --with-token <<< ${GITHUB_TOKEN} 

gh release create "${version_number}" --title "Release ${version_number}" --notes "${changelog_content}" --repo github.com/MOmarMiraj/onepassword-sdk-go
