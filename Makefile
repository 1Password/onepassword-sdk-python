PYTHON_VERSIONS := 3.9 3.10 3.11 3.12 3.13

release:
	src/release/scripts/release.sh

prep-release:
	src/release/scripts/prep-release.sh

build-wheels:
	src/release/scripts/build-wheels.sh $(PYTHON_VERSIONS)

release/install-dependencies:
# Check if pyenv is installed
	$(MAKE) check-pyenv-is-present
	
# Install all the python versions we support in one line
	pyenv install --skip-existing $(PYTHON_VERSIONS)

# Set pyenv local and install dependencies for each version
	for version in $(PYTHON_VERSIONS); do \
		pyenv local $$version; \
		pyenv exec pip3 install wheel setuptools build --break-system-packages; \
	done

check-pyenv-is-present:
	@command -v pyenv > /dev/null 2>&1 || { echo "pyenv is not installed.\nInstall it first (brew install pyenv) and rerun the command.\n\n"; exit 1; }
