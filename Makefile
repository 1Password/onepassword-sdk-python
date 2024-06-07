
check_if_gh_is_installed:
	@if ! command -v gh &> /dev/null; then\
		echo "gh is not installed";\
		exit 1;\
	fi

release:
	make check_if_gh_is_installed
	scripts/python_release.sh