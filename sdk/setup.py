from setuptools import setup, find_packages

setup(
    name='onepassword',
    version='0.1.0',
    packages=find_packages(),
    author='1Password',
    description="The 1Password Python SDK offers programmatic read access to your secrets in 1Password in an interface native to Python.",
    url='https://github.com/1Password/onepassword-sdk-python',
    install_requires=[
        "sdk_core_mac_arm64; platform_system=='Darwin' and platform_machine=='arm64'",
        "sdk_core_linux_x86_64; platform_system=='Linux' and platform_machine=='x86_64'",
    ],
)