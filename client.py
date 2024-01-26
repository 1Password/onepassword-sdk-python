import sys
import platform

# consts
SDKSemverVersion = "0010001" # v0.1.0
DefaultIntegrationName    = "Unknown"
DefaultIntegrationVersion = "Unknown"
SDKLanguage           = "Python"
DefaultRequestLibrary = "net/http"

class Client:
    def __init__(self, config, Secrets):
        self.config = config    # ClientConfig
        self.Secrets = Secrets  # SecretsApi 

class ClientConfig:
    def __init__(self, SAToken="", Language="", SDKLanguage="", IntegrationVersion="",
                 RequestLibraryName="", RequestLibraryVersion="", SystemOS="",
                 SystemOSVersion="", SystemArch=""):
        self.SAToken = SAToken
        self.Language = Language
        self.SDKVersion = SDKSemverVersion
        self.IntegrationVersion = IntegrationVersion
        self.RequestLibraryName = RequestLibraryName
        self.RequestLibraryVersion = RequestLibraryVersion
        self.SystemOS = SystemOS
        self.SystemOSVersion = SystemOSVersion
        self.SystemArch = SystemArch

def NewDefaultConfig():
    defaultOSVersion = "0.0.0"
    return ClientConfig(
		Language = SDKLanguage,
		SDKVersion= SDKSemverVersion,
		RequestLibraryName = DefaultRequestLibrary,
		RequestLibraryVersion = sys.version_info[0] + "." + sys.version_info[1] + "." + sys.version_info[2],
		SystemOS = platform.system(),
		SystemArch = platform.architecture()[0],
		SystemOSVersion = defaultOSVersion
    )
    
# def NewClient():
    # TODO

# def main():

# if __name__ == "__main__":
#     main()