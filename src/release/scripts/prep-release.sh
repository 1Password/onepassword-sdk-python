#!/bin/bash

# Helper script to prepare a release for the Python SDK.

output_version_file=".VERSION"
output_build_file="src/onepassword/build_number.py"
build_number_template_file="src/release/templates/build_number.tpl.py"


# Extracts the current build/version number for comparison and backup
current_version=$(cat "$output_version_file" | tr -d '[:space:]')
current_build=$(awk -F "['\"]" '/SDK_BUILD_NUMBER =/{print $2}' "$output_build_file" | tr -d '[:space:]')

# Function to execute upon exit
cleanup() {
    echo "Performing cleanup tasks..."
    # Revert changes to file if any
    echo -n "$current_version" > "$output_version_file"
    sed -e "s/{{ build }}/$current_build/" "$build_number_template_file" > "$output_build_file"
    exit 1
}

# Set the trap to call the cleanup function on exit
trap cleanup SIGINT

enforce_latest_code() {
    if [[ -n "$(git status --porcelain=v1)" ]]; then
        echo "ERROR: working directory is not clean."
        echo "Please stash your changes and try again."
        exit 1
    fi
}

# Function to validate the version number format x.y.z(-beta.w)
update_and_validate_version() {
    while true; do
        # Prompt the user to input the version number
        read -p "Enter the version number (format: x.y.z(-beta.w)): " version

        # Validate the version number format
        if [[ "${version}" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-beta\.[0-9]+)?$ ]]; then
            if [[ "${current_version}" != "${version}" ]]; then
                # TODO: Check the less than case as well.
                echo "New version number is: ${version}"
                return 0
            else
                echo "Version hasn't changed."
            fi
        else
            echo "Invalid version number format: ${version}"
            echo "Please enter a version number in the 'x.y.z(-beta.w)' format."
        fi
    done
}

# Function to validate the build number format.
# SEMVER Format: Mmmppbb - 7 Digits
update_and_validate_build() {
    while true; do
        # Prompt the user to input the build number
        read -p "Enter the build number (format: Mmmppbb): " build

        # Validate the build number format
        if [[ "${build}" =~ ^[0-9]{7}$ ]]; then
            if (( 10#$current_build < 10#$build )); then
                # Write the valid build number to the file
                echo "New build number is: ${build}"
                return 0
            else
                echo "New build version should be higher than current build version."
             fi
        else
            echo "Invalid build number format: ${build}"
            echo "Please enter a build number in the 'Mmmppbb' format."
        fi
    done
}

# Ensure that the current working directory is clean
enforce_latest_code

# Update and validate the version number
update_and_validate_version

# Update and validate the build number
update_and_validate_build

# Update version & build number in .VERSION and build_number.py respectively
echo -n "$version" > "$output_version_file"
sed  -e "s/{{ build }}/$build/" "$build_number_template_file" > "$output_build_file"


printf "Press ENTER to edit the RELEASE-NOTES in your default editor...\n"
read -r _ignore
${EDITOR:-nano} "src/release/RELEASE-NOTES"

# Get Current Branch Name
branch="$(git rev-parse --abbrev-ref HEAD)"

# if on main, then stash changes and create RC branch
if [[ "${branch}" = "main" ]]; then
    branch=rc/"${version}"
    git stash
    git fetch origin
    git checkout -b "${branch}"
    git stash apply
fi

# Add changes and commit/push to branch
git add .
git commit -S -m "Release v${version}"
git push --set-upstream origin "${branch}"

echo "Release has been prepared..
Make sure to double check version/build numbers in their appropriate files and
changelog is correctly filled out.
Once confirmed, run 'make release' to release the SDK!"

