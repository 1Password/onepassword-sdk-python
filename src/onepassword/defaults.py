import platform

SDK_LANGUAGE = "Python"
SDK_VERSION = "0010200"
DEFAULT_INTEGRATION_NAME = "Unknown"
DEFAULT_INTEGRATION_VERSION = "Unknown"
DEFAULT_REQUEST_LIBRARY = "reqwest"
DEFAULT_REQUEST_LIBRARY_VERSION = "0.11.24"
DEFAULT_OS_VERSION = "0.0.0"


# Generates a configuration dictionary with the user's parameters
def new_default_config(auth, integration_name, integration_version):
    client_config_dict = {
        "serviceAccountToken": auth,
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
    return client_config_dict
