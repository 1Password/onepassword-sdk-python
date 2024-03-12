import sys
import src.onepassword.client as onepassword
import os
import platform
import pytest

TOKEN = os.environ['OP_SERVICE_ACCOUNT_TOKEN']

## test resolve function

# valid
@pytest.mark.asyncio
async def test_valid_resolve():
    client = await onepassword.Client.authenticate(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    result = await client.secrets.resolve(reference="op://gowwbvgow7kxocrfmfvtwni6vi/6ydrn7ne6mwnqc2prsbqx4i4aq/password")
    assert(result == "test_password_42")

# invalid
@pytest.mark.asyncio
async def test_invalid_resolve():
    client = await onepassword.Client.authenticate(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    with pytest.raises(Exception, match="error resolving secret reference: secret reference is not prefixed with \"op://\""):
        await client.secrets.resolve(reference="invalid_reference")

## test client constructor
    
# valid
@pytest.mark.asyncio
async def test_good_client_construction():
    client = await onepassword.Client.authenticate(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    assert(client.config['serviceAccountToken'] == TOKEN)
    assert(client.config['integrationName'] == onepassword.DEFAULT_INTEGRATION_NAME)
    assert(client.config['integrationVersion'] == onepassword.DEFAULT_INTEGRATION_VERSION)

# invalid
@pytest.mark.asyncio
async def test_client_construction_no_auth():
    with pytest.raises(Exception, match='invalid client configuration: encountered the following errors: service account token was not specified; service account token had invalid format'):
        await onepassword.Client.authenticate(auth="", integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)

# invalid   
@pytest.mark.asyncio
async def test_client_construction_no_name():
    with pytest.raises(Exception, match='invalid client configuration: encountered the following errors: integration name was not specified'):
        await onepassword.Client.authenticate(auth=TOKEN, integration_name="", integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)

# invalid    
@pytest.mark.asyncio
async def test_client_construction_no_version():
    with pytest.raises(Exception, match='invalid client configuration: encountered the following errors: integration version was not specified'):
        await onepassword.Client.authenticate(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version="")

## test config function
    
# valid
def test_good_new_default_config():
    config = onepassword.new_default_config(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    
    assert(config["serviceAccountToken"] == TOKEN)
    assert(config["programmingLanguage"] == onepassword.SDK_LANGUAGE)
    assert(config["sdkVersion"] == onepassword.SDK_VERSION)
    assert(config["integrationName"] == onepassword.DEFAULT_INTEGRATION_NAME)
    assert(config["integrationVersion"] == onepassword.DEFAULT_INTEGRATION_VERSION)
    assert(config["requestLibraryName"] == onepassword.DEFAULT_REQUEST_LIBRARY)
    assert(config["requestLibraryVersion"] == platform.python_version())
    assert(config["os"] == platform.system().lower())
    assert(config["osVersion"] == onepassword.DEFAULT_OS_VERSION)
    assert(config["architecture"] == platform.machine())
