#!/bin/bash

# Helper script to prepare a release for the Python SDK.

output_version_file="version.py"
version_template_file="src/release/templates/version.tpl.py"

# The list of python verisons the SDKs release for
python_versions=("$@")

# Minimum glibc version we support
glibc_version=2-32

# These versions are being supported due to the SDKs supporting Python 3.9+
macOS_version_x86_64=10.9
macOS_version_arm64=11.0

# Extracts the current build/version number for comparison and backup 
current_version=$(awk -F "['\"]" '/SDK_VERSION =/{print $2}' "$output_version_file")

# Function to execute upon exit
cleanup() {
    echo "Performing cleanup tasks..."
    # Revert changes to file if any
    sed -e "s/{{ version }}/$current_version/" "$version_template_file" > "$output_version_file"
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

build_wheels() {
    os_platform=$1
    machine_platform=$2

    export PYTHON_OS_PLATFORM=$os_platform
    export PYTHON_MACHINE_PLATFORM=$machine_platform

    case "$os_platform" in 
        Darwin)
            macos_version=
            if [[ "$machine_platform" == "x86_64" ]]; then
                macos_version=$macOS_version_x86_64
            else
                macos_version=$macOS_version_arm64
            fi

            export _PYTHON_HOST_PLATFORM="macosx-${macos_version}-${PYTHON_MACHINE_PLATFORM}"
            ;;
        Linux)
            export _PYTHON_HOST_PLATFORM="manylinux-${glibc_version}-${PYTHON_MACHINE_PLATFORM}"
            ;;
        Windows)
            export _PYTHON_HOST_PLATFORM="win-${PYTHON_MACHINE_PLATFORM}"
            ;;
        *)
            echo "Unsupported OS: $os_platform"
            exit 1
            ;;
    esac

    pyenv exec python setup.py bdist_wheel
    rm -rf build
}

# Ensure working directory is clean
enforce_latest_code

# Update and validate the version number
update_and_validate_version

# Update version in version.py
sed  -e "s/{{ version }}/$version/" "$version_template_file" > "$output_version_file"

# Acquire the wheels for different OS
for python_version in "${python_versions[@]}"; do
pyenv local $python_version
build_wheels Darwin x86_64
build_wheels Darwin arm64
build_wheels Linux x86_64
build_wheels Linux aarch64
build_wheels Windows amd64
done

# Build Source as well incase wheels fails, pypi can install this as backup (standard practice)
python3 -m build --sdist

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

