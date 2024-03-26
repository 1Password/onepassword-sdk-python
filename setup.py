from setuptools import setup, find_packages
from sysconfig import get_platform

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False
            self.plat_name = get_platform()
except ImportError:
    bdist_wheel = None

def get_included_core():
    # Return the correct C extension for the given platform
    return ["lib/aarch64/libop_uniffi_core.so", "lib/aarch64/op_uniffi_core.py"]

setup(
    name='onepassword',
    version='0.1.0-beta.1',
    author='1Password',
    description="The 1Password Python SDK offers programmatic read access to your secrets in 1Password in an interface native to Python.",
    url='https://github.com/1Password/onepassword-sdk-python',
    packages=find_packages(
        where='src',
    ),
    package_dir={"": "src"},
    cmdclass={'bdist_wheel': bdist_wheel},
    package_data={"": get_included_core()},
) 