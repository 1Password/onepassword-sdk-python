from pathlib import Path
from setuptools import setup, find_packages
from sysconfig import get_platform
from version import SDK_VERSION
import platform
import os

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
            # This platform naming is sufficient for distributing this package via source cloning (e.g. pip + GitHub) since the wheel will be built locally
            # for each user's platform: https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/#basic-platform-tags
            self.plat_name = get_platform().translate({"-": "_", ".": "_"})
            self.plat_name_supplied = True
except ImportError:
    bdist_wheel = None


def get_shared_library_data_to_include():
    # Return the correct uniffi C shared library extension for the given platform
    include_path = "lib"
    machine_type = os.getenv("PYTHON_MACHINE_PLATFORM") or platform.machine().lower()
    if machine_type in ["x86_64", "amd64"]:
        include_path = os.path.join(include_path, "x86_64")
    elif machine_type in ["aarch64", "arm64"]:
        include_path = os.path.join(include_path, "aarch64")

    # Map current platform to the correct shared library file name
    platform_to_lib = {
        "Darwin": "libop_uniffi_core.dylib",
        "Linux": "libop_uniffi_core.so",
        "Windows": "op_uniffi_core.dll",
    }
    platform_name = os.getenv("PYTHON_OS_PLATFORM") or platform.system()
    c_shared_library_file_name = platform_to_lib.get(platform_name, "")
    c_shared_library_file_name = os.path.join(include_path, c_shared_library_file_name)

    uniffi_bindings_file_name = "op_uniffi_core.py"
    uniffi_bindings_file_name = os.path.join(include_path, uniffi_bindings_file_name)

    return [c_shared_library_file_name, uniffi_bindings_file_name]


setup(
    name="onepassword-sdk",
    version=SDK_VERSION,
    author="1Password",
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    description="The 1Password Python SDK offers programmatic read access to your secrets in 1Password in an interface native to Python.",
    url="https://github.com/1Password/onepassword-sdk-python",
    packages=find_packages(
        where="src",
    ),
    license="MIT",
    license_files="LICENSE",
    package_dir={"": "src"},
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={"bdist_wheel": bdist_wheel},
    package_data={"": get_shared_library_data_to_include()},
    install_requires=[
        "pydantic>=2.5",  # Minimum Pydantic version to run the Python SDK
    ],
)
