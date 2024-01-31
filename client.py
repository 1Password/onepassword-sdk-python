import sys
import platform

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
    
# def NewClient():
    # TODO

# def createClient():
    # TODO

def WithServiceAccountToken(token):
    def assign(client):
        client.config.SAToken = token
    return assign

def WithIntegrationInfo(name, version):
    def assign(client):
        client.config.IntegrationName = name
        client.config.IntegrationVersion = version
    return assign

# def main():

# if __name__ == "__main__":
#     main()