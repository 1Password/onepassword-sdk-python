import platform
from onepassword.build_number import SDK_BUILD_NUMBER

SDK_LANGUAGE = "Python"
SDK_VERSION = SDK_BUILD_NUMBER
DEFAULT_INTEGRATION_NAME = "Unknown"
DEFAULT_INTEGRATION_VERSION = "Unknown"
DEFAULT_REQUEST_LIBRARY = "reqwest"
DEFAULT_REQUEST_LIBRARY_VERSION = "0.11.24"
DEFAULT_OS_VERSION = "0.0.0"


class DesktopAuth:
    def __init__(self, account_name: str):
        """
        Initialize a DesktopAuth instance.

        Args:
            account_name (str): The name of the account.
        """
        self.account_name = account_name


# Generates a configuration dictionary with the user's parameters
def new_default_config(auth: DesktopAuth | str, integration_name, integration_version):
    client_config_dict = {
        "programmingLanguage": SDK_LANGUAGE,
        "sdkVersion": SDK_VERSION,
        "integrationName": integration_name,
        "integrationVersion": integration_version,
        "requestLibraryName": DEFAULT_REQUEST_LIBRARY,
        "requestLibraryVersion": DEFAULT_REQUEST_LIBRARY_VERSION,
        "os": platform.system().lower(),
        "osVersion": DEFAULT_OS_VERSION,
        "architecture": platform.machine(),
    }
    if not isinstance(auth, DesktopAuth):
        client_config_dict["serviceAccountToken"] = auth

    return client_config_dict
