#!/bin/bash

# Helper script to prepare a Python Release for the SDKs.

set -e

# Check if Github CLI is installed
if ! command -v gh &> /dev/null; then
	echo "gh is not installed";\
	exit 1;\
fi

# Read the version number and build number from the respective files
version_number=$(< src/onepassword/version)
build_number=$(< src/onepassword/version-build)

# Function to validate the version number format x.y.z(-beta.w)
validate_version_number() {
    local version="$1"
    local version_file="src/onepassword/version"
    while true; do
        if [[ "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-beta\.[0-9]+)?$ ]]; then
            echo "Updated version number is: ${version}"
            return 0
        else
            echo "Invalid version number format: ${version}"
            echo "Please update the version number in the '${version_file}' file."
            ${EDITOR:-nano} "${version_file}"
            version=$(<"${version_file}")
        fi
    done
}

# Function to validate the build number format.
# SEMVER Format: Mmmppbb - 7 Digits 
validate_build_number() {
    local build="$1"
    local build_file="src/onepassword/version-build"
    while true; do
        if [[ "${build}" =~ ^[0-9]{7}$ ]]; then
            echo "Updated build number is: ${build}"
            return 0
        else
            echo "Invalid build number format: ${build}"
            echo "Please update the build number in the 'internal/version-build' file."
            ${EDITOR:-nano} "${build_file}"
            build=$(< "${build_file}")
        fi
    done
}

# Validate the version number 
validate_version_number "$version_number"

# Validate build number
validate_build_number "$build_number"

# Prompt the user to input multiline text
echo "Enter your changelog for the release (press Ctrl+D when finished):"
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

# Ensure GITHUB_CLI_TOKEN env var is set
if [ -z "${GITHUB_CLI_TOKEN}" ]; then
  echo "GITHUB_CLI_TOKEN environment variable is not set."
  exit 1
fi

# Login with Github CLI
gh auth login --with-token <<< ${GITHUB_CLI_TOKEN} 

gh release create "${version_number}" --title "Release ${version_number}" --notes "${changelog_content}" --repo github.com/1Password/onepassword-sdk-python