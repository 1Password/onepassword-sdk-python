import sys
import platform
from core import *
from secrets_api import SecretsSource

sdk_version = "0010001"  # v0.1.0
default_integration_name = "Unknown"
default_integration_version = "Unknown"
sdk_language = "Python"
default_request_library = "net/http"
default_os_version = "0.0.0"


class Client:
    def __init__(self, auth="", integration_name="", integration_version=""):
        self.auth = auth  # onepassword.ServiceAccountCredentials("ops_..."),
        self.integration_name = integration_name,
        self.integration_version = integration_version,

        # one possible way of passing the client ID
        self.config = NewDefaultConfig(),
        self.secrets = SecretsSource(clientID=InitClient(self.config)),


def NewDefaultConfig():
    client_config_dict = {
        "SAToken": "",
        "Language": sdk_language,
        "SDKVersion": sdk_version,
        "IntegrationName": "",
        "IntegrationVersion": "",
        "RequestLibraryName": default_request_library,
        "RequestLibraryVersion": sys.version_info[0] + "." + sys.version_info[1] + "." + sys.version_info[2],
        "SystemOS": platform.system(),
        "SystemOSVersion": platform.architecture()[0],
        "SystemArch": default_os_version,
    }
    return client_config_dict
