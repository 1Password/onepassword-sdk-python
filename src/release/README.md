## How to Prepare a Release for the Python SDK

Before running this script, the user must make sure that they have the write permissions to the Python SDK repository.

Run this make command to install all dependencies required for the Python SDK release process.
```
make release/install-dependencies
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