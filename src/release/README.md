# How to Release the Python SDK

## Release off an Release Candidate Branch in Github Actions
To release the Python SDK via Github Action, you must do the following:
1. SDK core opens a new PR with the latest generated code and latest core. This branch should start off with `sdk-core/...`
2. Add the release notes for the RC as well as update the examples if needed.
3. Run the `Release Python SDKs` action and input the correct build and version number while referencing the RC branch.
4. After the action is completed, the Python SDK is released on Github and PyPi, you can merge the PR branch.

If the Github Action isn't working, you can follow the manual steps below to release the Python SDK.

## Manual Steps to release a Python SDK
Before running this script, the user must make sure that they have the write permissions to the Python SDK repository.

Run this make command to install all dependencies required for the Python SDK release process.
```
release/install-dependencies
```

Step 1. Make any changes to the SDK as required on a feature branch or main branch.
NOTE: If ran on a main branch, a release branch will be created.

Step 2. Go to the root of the repo and run
```
make prep-release
```
Follow the scripts instructions and the release has now been prepped.

Step 3. Ensure that the correct files have been updated - i.e. version/build files, release-notes has been updated. Check the latest commit on the branch to see your changes.

Step 4. To build the wheels and source distribution for PyPi, run in the root of the repo:
```
make build-wheels
```

Step 5. Ensure your GITHUB_TOKEN environment variable is set as this will allow you to create the tags/release and push it.

Step 6. Ensure you have the PyPi credentials to login when uploading the source and wheels to PyPi.

Step 7. If everything looks good, at the root of the repo, run:
```
make release
```
Step 8. Congratulations, you have released the newest Python SDK!