#!/bin/bash

# Helper script to prepare a Python Release for the SDKs.

set -e

# Function to validate the version number format x.y.z(-beta.w)
validate_version_number() {
    local version="$1"
    if [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-beta\.[0-9]+)?$ ]]; then
        return 0
    else
        return 1
    fi
}

# Function to validate the build number format Mmmppbb
validate_build_number() {
    local build="$1"
    if [[ "$build" =~ ^[0-9]{1}[0-9]{2}[0-9]{2}[0-9]{2}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Read and validate the version number
while true; do
    read -p "Please provide the version number (x.y.z(-beta.w)): " version_number
    if validate_version_number "$version_number"; then
      break
   else
      echo "Invalid version number format. Please try again."
    fi
done

# Read and validate the build number
while true; do
    read -p "Please provide the build number (Mmmppbb): " build_number
    if  validate_build_number "$build_number"; then
      break    
   else
      echo "Invalid build number format. Please try again."
   fi
done

# Replace setup.py with new version number
awk -v version="$version_number" '
  /version/ && !done {
    print "    version=\"" version "\"";
    done = 1;
    next;
  } 
  { print }' setup.py > tmpfile && mv tmpfile setup.py

# Replace defaults.py with new version number
awk -v version="$version_number" -v build="$build_number" '
  /SDK_VERSION/ && !done {
    print "SDK_VERSION = ", "\"" build "\" # v" version;
    done = 1;
    next;
  } 
  { print }' src/onepassword/defaults.py > tmpfile && mv tmpfile src/onepassword/defaults.py
# Prompt the user to input multiline text
echo "Enter your multiline text (press Ctrl+D when finished):"
changelog_content=""

# Read multiline input from the user until Ctrl+D is pressed
while IFS= read -r line; do
    changelog_content+="$line"$'\n' # Append each line to the variable with a newline character
done

git tag -a -s  "v${version_number}" -m "${version_number}"
git status
git commit -am "Release for ${version_number}"
git push 

# Login with Github CLI
gh auth login --with-token <<< ${GIT_TOKEN} 

gh release create "${version_number}" --title "Release ${version_number}" --notes "${changelog_content}" --repo github.com/1Password/onepassword-sdk-python
 


