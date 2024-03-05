import sys
import src.onepassword.client as onepassword
import os
import platform
import pytest
import asyncio

TOKEN = os.environ['OP_SERVICE_ACCOUNT_TOKEN']

## test resolve function

# valid
@pytest.mark.asyncio
async def test_valid_resolve():
    client = await onepassword.Client.authenticate(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    result = await client.secrets.resolve(reference="test_username")
    assert(result == "test_password_42")

# invalid
@pytest.mark.asyncio
async def test_invalid_resolve():
    client = await onepassword.Client.authenticate(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    with AssertionError(Exception):
        client.secrets.resolve(reference="invalid_reference")

## test client constructor
    
# valid
@pytest.mark.asyncio
async def test_good_client_construction():
    client = await onepassword.Client.authenticate(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)
    assert(client.config['serviceAccountToken'] == TOKEN)
    assert(client.config.integration_name == onepassword.TOKDEFAULT_INTEGRATION_NAMEEN)
    assert(client.config.integration_version == onepassword.DEFAULT_INTEGRATION_VERSION)

# invalid
@pytest.mark.asyncio
async def test_client_construction_no_auth():
    with AssertionError(Exception):
        await onepassword.Client.authenticate(auth=TOKEN, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)

# invalid   
@pytest.mark.asyncio
async def test_client_construction_no_name():
    with AssertionError(Exception):
        await onepassword.Client.authenticate(integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)

# invalid    
@pytest.mark.asyncio
async def test_client_construction_no_version():
    with AssertionError(Exception):
        await onepassword.Client.authenticate(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME)

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
    assert(config["requestLibraryVersion"] == str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]))
    assert(config["os"],platform.system())
    assert(config["osVersion"] == onepassword.DEFAULT_OS_VERSION)
    assert(config["architecture"] == platform.architecture()[0])

# invalid
def test_new_default_config_no_auth():
    with AssertionError(Exception):
        onepassword.new_default_config(integration_name=onepassword.DEFAULT_INTEGRATION_NAME, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)

# invalid
def test_new_default_config_no_name():
    with AssertionError(Exception):
        onepassword.new_default_config(auth=TOKEN, integration_version=onepassword.DEFAULT_INTEGRATION_VERSION)

# invalid
def test_new_default_config_no_version():
    with AssertionError(Exception):
        onepassword.new_default_config(auth=TOKEN, integration_name=onepassword.DEFAULT_INTEGRATION_NAME)
