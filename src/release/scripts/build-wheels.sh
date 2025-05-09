#!/bin/bash

# Helper script to build the required wheels for the Python SDK

# The list of python verisons the SDKs release for
python_versions=("$@")

# Minimum glibc version we support
glibc_version=2-32

# These versions are being supported due to the SDKs supporting Python 3.9+
macOS_version_x86_64=10.9
macOS_version_arm64=11.0

# Extracts the current verison number for cleanup function
current_version=$(cat .VERSION)

# Function to execute upon exit
cleanup() {
    echo "Performing cleanup tasks..."
    # Remove dist and egg-info and the potential release candidate if created
    rm -r dist src/*.egg-info/ onepassword_sdk-"${current_version}"
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

build_wheels() {
    os_platform=$1
    machine_platform=$2

    export PYTHON_OS_PLATFORM=$os_platform
    export PYTHON_MACHINE_PLATFORM=$machine_platform

    case "$os_platform" in
        Darwin)
            macos_version=
            # Min MacOS version for Python 3.13+ is 10.13
            python_version=$(pyenv exec python3 --version 2>&1)

            if [[ "$machine_platform" == "x86_64" ]]; then
                if [[ "$python_version" == "Python 3.13"* ]]; then
                macos_version="10.13"
            else
                macos_version=$macOS_version_x86_64
            fi
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

    pyenv exec python3 -m build --wheel
    rm -rf build
}

# Ensure that the current working directory is clean and building of wheels is made off of latest main
enforce_latest_code

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
pyenv exec python3 -m build --sdist