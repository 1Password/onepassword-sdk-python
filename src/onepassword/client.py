import sys
import platform
from core import *
from secrets_api import Secrets
import asyncio
import weakref

SDK_LANGUAGE = "Go"
SDK_VERSION = "0010001"  # v0.1.0
DEFAULT_INTEGRATION_NAME = "Unknown"
DEFAULT_INTEGRATION_VERSION = "Unknown"
DEFAULT_REQUEST_LIBRARY = "net/http"
DEFAULT_OS_VERSION = "0.0.0"


class Client:

    """authenticate verifies the user's permissions and allows them to access their secrets."""
    @classmethod
    async def authenticate(cls, auth, integration_name, integration_version):
        self = cls()
        self.config = new_default_config(auth=auth, integration_name=integration_name, integration_version=integration_version)
        self.client_id = int(await InitClient(self.config))
        self.secrets = Secrets(client_id=self.client_id)
        self._finalizer = weakref.finalize(self, ReleaseClient, self.client_id)

        return self

# Generates a configuration dictionary with the user's parameters
def new_default_config(auth, integration_name, integration_version):
    client_config_dict = {
        "serviceAccountToken": auth,
        "programmingLanguage": SDK_LANGUAGE,
        "sdkVersion": SDK_VERSION,
        "integrationName": integration_name,
        "integrationVersion": integration_version,
        "requestLibraryName": DEFAULT_REQUEST_LIBRARY,
        "requestLibraryVersion": str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]),
        "os": platform.system(),
        "osVersion": DEFAULT_OS_VERSION,
        "architecture": platform.architecture()[0],
    }
    return client_config_dict
