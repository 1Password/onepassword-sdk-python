#!/bin/bash

# Helper script to prepare a release for the Python SDK.

# Read the build number from version-build to ensure that the build number has been updated

output_setup_file="setup.py"
output_defaults_file="src/onepassword/defaults.py"
setup_template_file="templates/setup.tpl.py"
defaults_template_file="templates/defaults.tpl.py"

# Extracts the current build number for comparison 
current_build_number=$(awk -F "['\"]" '/SDK_VERSION =/{print $2}' "$output_defaults_file")

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
            # Write the valid version number to the file
            echo "New version number is: ${version}"
            return 0
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
            # Write the valid build number to the file
            echo "New build number is: ${build}"
            return 0
        else
            echo "Invalid build number format: ${build}"
            echo "Please enter a build number in the 'Mmmppbb' format."
        fi
    done
}

# Ensure working directory is clean
enforce_latest_code

# Update and validate the version number
update_and_validate_version

# Update and validate the build number
update_and_validate_build 

if [[ "$current_build_number" == "$build" ]]; then
    echo "Build version hasn't changed. Stopping." >&2
    exit 1
fi

# Update version number in setup.py
sed -e "s/{{ VERSION }}/$version/" "$setup_template_file" > "$output_setup_file"

# Update version number in defaults.py
sed -e "s/{{ BUILD }}/$build/" -e "s/{{ VERSION }}/$version/" "$defaults_template_file" > "$output_defaults_file"

echo "Enter your changelog for the release (press Ctrl+D when finished):"

# Read changelog input from the user until Ctrl+D is pressed
changelog_content=""
while IFS= read -r line; do
    changelog_content+="${line}"$'\n' # Append each line to the variable with a newline character
done

changelog_file="src/onepassword/changelogs/"${version}"-"${build}""

# Store the changelog input into a file
echo "${changelog_content}" >> "${changelog_file}"

echo "Release has been prepared..
Make sure to double check version/build numbers in their appropriate files and
changelog is correctly filled out.
Once confirmed, run 'make release' to release the SDK!"

