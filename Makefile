PYTHON_VERSIONS := 3.9 3.10 3.11 3.12

release:
	src/release/scripts/release.sh

prep-release:
	src/release/scripts/prep-release.sh $(PYTHON_VERSIONS)

release/install-dependencies:
# Install pyenv
	brew install pyenv

# Install build
	pip install build --break-system-packages
	
# Install all the python versions we support in one line
	pyenv install --skip-existing $(PYTHON_VERSIONS)

# Set pyenv local and install dependencies for each version
	for version in $(PYTHON_VERSIONS); do \
		pyenv local $$version; \
		pyenv exec pip install wheel setuptools; \
	done