import unittest
from sdk import client as onepassword
import os

TOKEN = os.environ['OP_SERVICE_ACCOUNT_TOKEN']

class TestPythonSDKClient(unittest.TestCase):
    ## test resolve function

    # valid
    def test_valid_resolve(self):
        client = onepassword.Client(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
        result = client.secrets.resolve(reference="test_username")
        self.assertEqual(result, "password")  # "password" is a temporary placeholder, replace with actual secret value
    
    # invalid
    def test_invalid_resolve(self):
        client = onepassword.Client(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
        result = client.secrets.resolve(reference="invalid_reference")

    ## test client constructor
        
    # valid
    def test_good_client_construction(self):
        client = onepassword.Client(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    
    # invalid
    def test_client_construction_no_auth(self):
        client = onepassword.Client(auth=TOKEN, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    
    # invalid   
    def test_client_construction_no_name(self):
        client = onepassword.Client(integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    
    # invalid    
    def test_client_construction_no_version(self):
        client = onepassword.Client(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME)

    ## test config function
        
    # valid
    def test_good_new_default_config(self):
        config = onepassword.new_default_config(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
        
        # the commented out assertions may be untestable as they are device-specific
        self.assertEqual(config["SAToken"], TOKEN)
        self.assertEqual(config["Language"], onepassword.SDK_LANGUAGE)
        self.assertEqual(config["SDKVersion"], onepassword.SDK_VERSION)
        self.assertEqual(config["IntegrationName"], onepassword.DEFAULT_INTEGRATION_NAME)
        self.assertEqual(config["IntegrationVersion"], onepassword.DEFAULT_INTEGRATION_VERSION)
        self.assertEqual(config["RequestLibraryName"], onepassword.DEFAULT_REQUEST_LIBRARY)
        # self.assertEqual(config["RequestLibraryVersion"], )
        # self.assertEqual(config["SystemOS"],)
        self.assertEqual(config["SystemOSVersion"], onepassword.DEFAULT_OS_VERSION)
        # self.assertEqual(config["SystemArch"], )
    
    # invalid
    def test_new_default_config_no_auth(self):
        config = onepassword.new_default_config(integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    
    # invalid
    def test_new_default_config_no_name(self):
        config = onepassword.new_default_config(auth=TOKEN, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    
    # invalid
    def test_new_default_config_no_version(self):
        config = onepassword.new_default_config(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME)
        
if __name__ == '__main__':
    unittest.main()