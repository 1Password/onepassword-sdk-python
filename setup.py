from setuptools import setup, find_packages
from sysconfig import get_platform
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
except ImportError:
    bdist_wheel = None


def get_shared_library_data_to_include():
    # Return the correct uniffi C shared library extension for the given platform
    include_path = "lib"
    if platform.machine().lower() == "x86_64" or platform.machine().lower() == "amd64":
        include_path = os.path.join(include_path, "x86_64")
    elif (
        platform.machine().lower() == "aarch64" or platform.machine().lower() == "arm64"
    ):
        include_path = os.path.join(include_path, "aarch64")

    c_shared_library_file_name = ""
    if platform.system() == "Darwin":
        c_shared_library_file_name = "libop_uniffi_core.dylib"
    elif platform.system() == "Linux":
        c_shared_library_file_name = "libop_uniffi_core.so"
    elif platform.system() == "Windows":
        c_shared_library_file_name = "op_uniffi_core.dll"

    c_shared_library_file_name = os.path.join(include_path, c_shared_library_file_name)

    uniffi_bindings_file_name = "op_uniffi_core.py"
    uniffi_bindings_file_name = os.path.join(include_path, uniffi_bindings_file_name)

    return [c_shared_library_file_name, uniffi_bindings_file_name]


setup(
    name="onepassword",
    version="0.1.0-beta.1",
    author="1Password",
    description="The 1Password Python SDK offers programmatic read access to your secrets in 1Password in an interface native to Python.",
    url="https://github.com/1Password/onepassword-sdk-python",
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    cmdclass={"bdist_wheel": bdist_wheel},
    package_data={"": get_shared_library_data_to_include()},
)
