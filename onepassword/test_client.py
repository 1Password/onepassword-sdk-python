import sys
from onepassword.client import Client, new_default_config, DEFAULT_INTEGRATION_NAME, DEFAULT_INTEGRATION_VERSION, SDK_LANGUAGE, SDK_VERSION, DEFAULT_OS_VERSION, DEFAULT_REQUEST_LIBRARY
import os
import platform
import pytest

TOKEN = os.getenv('OP_SERVICE_ACCOUNT_TOKEN')

## test resolve function

# valid
@pytest.mark.asyncio
async def test_valid_resolve():
    client = await Client.authenticate(auth=TOKEN, integration_name=DEFAULT_INTEGRATION_NAME, integration_version=DEFAULT_INTEGRATION_VERSION)
    result = await client.secrets.resolve(reference="op://gowwbvgow7kxocrfmfvtwni6vi/6ydrn7ne6mwnqc2prsbqx4i4aq/password")
    assert(result == "test_password_42")

# invalid
@pytest.mark.asyncio
async def test_invalid_resolve():
    client = await Client.authenticate(auth=TOKEN, integration_name=DEFAULT_INTEGRATION_NAME, integration_version=DEFAULT_INTEGRATION_VERSION)
    with pytest.raises(Exception, match="error resolving secret reference: secret reference is not prefixed with \"op://\""):
        await client.secrets.resolve(reference="invalid_reference")

## test client constructor
    
# valid
@pytest.mark.asyncio
async def test_good_client_construction():
    client = await Client.authenticate(auth=TOKEN, integration_name=DEFAULT_INTEGRATION_NAME, integration_version=DEFAULT_INTEGRATION_VERSION)
    assert(client.config['serviceAccountToken'] == TOKEN)
    assert(client.config['integrationName'] == DEFAULT_INTEGRATION_NAME)
    assert(client.config['integrationVersion'] == DEFAULT_INTEGRATION_VERSION)

# invalid
@pytest.mark.asyncio
async def test_client_construction_no_auth():
    with pytest.raises(Exception, match='invalid client configuration: encountered the following errors: service account token was not specified; service account token had invalid format'):
        await Client.authenticate(auth="", integration_name=DEFAULT_INTEGRATION_NAME, integration_version=DEFAULT_INTEGRATION_VERSION)

# invalid   
@pytest.mark.asyncio
async def test_client_construction_no_name():
    with pytest.raises(Exception, match='invalid client configuration: encountered the following errors: integration name was not specified'):
        await Client.authenticate(auth=TOKEN, integration_name="", integration_version=DEFAULT_INTEGRATION_VERSION)

# invalid    
@pytest.mark.asyncio
async def test_client_construction_no_version():
    with pytest.raises(Exception, match='invalid client configuration: encountered the following errors: integration version was not specified'):
        await Client.authenticate(auth=TOKEN, integration_name=DEFAULT_INTEGRATION_NAME, integration_version="")

## test config function
    
# valid
def test_good_new_default_config():
    config = new_default_config(auth=TOKEN, integration_name=DEFAULT_INTEGRATION_NAME, integration_version=DEFAULT_INTEGRATION_VERSION)
    
    assert(config["serviceAccountToken"] == TOKEN)
    assert(config["programmingLanguage"] == SDK_LANGUAGE)
    assert(config["sdkVersion"] == SDK_VERSION)
    assert(config["integrationName"] == DEFAULT_INTEGRATION_NAME)
    assert(config["integrationVersion"] == DEFAULT_INTEGRATION_VERSION)
    assert(config["requestLibraryName"] == DEFAULT_REQUEST_LIBRARY)
    assert(config["requestLibraryVersion"] == str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]))
    assert(config["os"] == platform.system().lower())
    assert(config["osVersion"] == DEFAULT_OS_VERSION)
    assert(config["architecture"] == platform.machine())
