import onepassword.client as onepassword
import onepassword.defaults as onepassword_defaults
import os
import platform
import pytest

TOKEN = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")

## test resolve function


# valid
@pytest.mark.asyncio
async def test_valid_resolve():
    client = await onepassword.Client.authenticate(
        auth=TOKEN,
        integration_name=onepassword_defaults.DEFAULT_INTEGRATION_NAME,
        integration_version=onepassword_defaults.DEFAULT_INTEGRATION_VERSION,
    )
    result = await client.secrets.resolve(
        secret_reference="op://gowwbvgow7kxocrfmfvtwni6vi/6ydrn7ne6mwnqc2prsbqx4i4aq/password"
    )
    assert result == "test_password_42"


# invalid
@pytest.mark.asyncio
async def test_invalid_resolve():
    client = await onepassword.Client.authenticate(
        auth=TOKEN,
        integration_name=onepassword_defaults.DEFAULT_INTEGRATION_NAME,
        integration_version=onepassword_defaults.DEFAULT_INTEGRATION_VERSION,
    )
    with pytest.raises(
        Exception,
        match='error resolving secret reference: the secret reference could not be parsed: secret reference is not prefixed with "op://"',
    ):
        await client.secrets.resolve(secret_reference="invalid_reference")


## test client constructor


# invalid
@pytest.mark.asyncio
async def test_client_construction_no_auth():
    with pytest.raises(
        Exception,
        match="invalid user input: encountered the following errors: service account token was not specified; service account token had invalid format",
    ):
        await onepassword.Client.authenticate(
            auth="",
            integration_name=onepassword_defaults.DEFAULT_INTEGRATION_NAME,
            integration_version=onepassword_defaults.DEFAULT_INTEGRATION_VERSION,
        )


# invalid
@pytest.mark.asyncio
async def test_client_construction_no_name():
    with pytest.raises(
        Exception,
        match="invalid user input: encountered the following errors: integration name was not specified",
    ):
        await onepassword.Client.authenticate(
            auth=TOKEN,
            integration_name="",
            integration_version=onepassword_defaults.DEFAULT_INTEGRATION_VERSION,
        )


# invalid
@pytest.mark.asyncio
async def test_client_construction_no_version():
    with pytest.raises(
        Exception,
        match="invalid user input: encountered the following errors: integration version was not specified",
    ):
        await onepassword.Client.authenticate(
            auth=TOKEN,
            integration_name=onepassword_defaults.DEFAULT_INTEGRATION_NAME,
            integration_version="",
        )


## test config function


# valid
def test_good_new_onepassword_default_config():
    config = onepassword.new_default_config(
        auth=TOKEN,
        integration_name=onepassword_defaults.DEFAULT_INTEGRATION_NAME,
        integration_version=onepassword_defaults.DEFAULT_INTEGRATION_VERSION,
    )

    assert config["serviceAccountToken"] == TOKEN
    assert config["programmingLanguage"] == onepassword_defaults.SDK_LANGUAGE
    assert config["sdkVersion"] == onepassword_defaults.SDK_VERSION
    assert config["integrationName"] == onepassword_defaults.DEFAULT_INTEGRATION_NAME
    assert (
        config["integrationVersion"] == onepassword_defaults.DEFAULT_INTEGRATION_VERSION
    )
    assert config["requestLibraryName"] == onepassword_defaults.DEFAULT_REQUEST_LIBRARY
    assert (
        config["requestLibraryVersion"]
        == onepassword_defaults.DEFAULT_REQUEST_LIBRARY_VERSION
    )
    assert config["os"] == platform.system().lower()
    assert config["osVersion"] == onepassword_defaults.DEFAULT_OS_VERSION
    assert config["architecture"] == platform.machine()
