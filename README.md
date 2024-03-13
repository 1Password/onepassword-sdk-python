# 1Password Python SDK

> ❗ This project is still in its early, pre-alpha stages of development. Its stability is not yet fully assessed, and future iterations may bring backwards incompatible changes. Proceed with caution.

The 1Password Python SDK offers programmatic read access to your secrets in 1Password in an interface native to Python. The SDK currently supports authentication with [1Password Service Accounts](https://developer.1password.com/docs/service-accounts/).

## Get started

To use the 1Password Python SDK in your project:

1. [Create a 1Password Service Account](https://developer.1password.com/docs/service-accounts/get-started/#create-a-service-account). Make sure to grant the service account access to the vaults where the secrets your project needs access to are stored.
2. Export your service account token to the `OP_SERVICE_ACCOUNT_TOKEN` environment variable:

```bash
export OP_SERVICE_ACCOUNT_TOKEN=<your-service-account-token>
```

3. In your project, download the 1Password Python SDK:

```bash
python -m pip install 'onepassword @ git+https://https://github.com/1Password/onepassword-sdk-python'
```

4. Use the SDK in your project:

```python
import asyncio
import os
from onepassword.client import Client, DEFAULT_INTEGRATION_NAME, DEFAULT_INTEGRATION_VERSION

async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    
    # Connects to 1Password.
    client = await Client.authenticate(auth=token, integration_name=DEFAULT_INTEGRATION_NAME, integration_version=DEFAULT_INTEGRATION_VERSION)
   
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://xw33qlvug6moegr3wkk5zkenoa/bckakdku7bgbnyxvqbkpehifki/foobar")
    print(value)

if __name__ == '__main__':
    asyncio.run(main())

```

Make sure to use [secret reference URIs](https://developer.1password.com/docs/cli/secret-references/) with the syntax `op://vault/item/field` to securely load secrets from 1Password into your code.