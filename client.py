import sys
import platform
import ctypes
import op_sdk_core_py
from core import *
from secrets_api import SecretsSource

# consts
SDKVersion = "0010001" # v0.1.0
DefaultIntegrationName    = "Unknown"
DefaultIntegrationVersion = "Unknown"
SDKLanguage           = "Python"
DefaultRequestLibrary = "net/http"

# configuration dictionary
clientConfigDict = {
    "SAToken" : "",
    "Language" : "",
    "SDKVersion" : "",
    "IntegrationName" : "",
    "IntegrationVersion" : "",
    "RequestLibraryName" : "",
    "RequestLibraryVersion" : "",
    "SystemOS" : "",
    "SystemOSVersion" : "",
    "SystemArch" : "",
}

class Client:
    def __init__(self, auth="", integration_name="", integration_version=""):
        self.auth = auth   ## onepassword.ServiceAccountCredentials("ops_..."),
        self.integration_name = integration_name,
        self.integration_version = integration_version,

        # one possible way of passing the client ID
        self.config = NewDefaultConfig(),
        self.secrets = SecretsSource(clientID=InitClient(self.config)),

def NewDefaultConfig():
    defaultOSVersion = "0.0.0"

    newConfigDict = clientConfigDict
    newConfigDict["Language"] = SDKLanguage
    newConfigDict["SDKVersion"] = SDKVersion
    newConfigDict["RequestLibraryName"] = DefaultRequestLibrary
    newConfigDict["RequestLibraryVersion"] = sys.version_info[0] + "." + sys.version_info[1] + "." + sys.version_info[2]
    newConfigDict["SystemOS"] = platform.system()
    newConfigDict["SystemArch"] = platform.architecture()[0],
    newConfigDict["SystemOSVersion"] = defaultOSVersion
    
    return newConfigDict

def main():

    print(InitClient())
    print(Invoke())
    ReleaseClient()

if __name__ == "__main__":
    main()