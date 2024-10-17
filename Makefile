PYTHON_VERSIONS := 3.9 3.10 3.11 3.12 3.13

release:
	src/release/scripts/release.sh

prep-release:
	src/release/scripts/prep-release.sh

build-wheels:
	src/release/scripts/build-wheels.sh $(PYTHON_VERSIONS)

release/install-dependencies:
# Install latest version of pyenv if not already installed
	brew install pyenv
	
# Install all the python versions we support in one line
	pyenv install --skip-existing $(PYTHON_VERSIONS)

# Set pyenv local and install dependencies for each version
	for version in $(PYTHON_VERSIONS); do \
		pyenv local $$version; \
		pyenv exec pip3 install wheel setuptools build --break-system-packages; \
	done

