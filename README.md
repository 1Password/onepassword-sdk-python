<p align="center">
  <a href="https://1password.com">
      <h1 align="center">1Password Python SDK (beta)</h1>
  </a>
</p>

<p align="center">
 <h4 align="center"> ❗ The 1Password SDK project is in beta. Future iterations may bring backwards-incompatible changes.</h4>
</p>

<p align="center">
  <a href="https://developer.1password.com/docs/sdks/">Documentation</a> | <a href="https://github.com/1Password/onepassword-sdk-python/tree/main/example">Examples</a>
<br/>

---

The 1Password Python SDK offers programmatic access to your secrets in 1Password with Python. During the beta, you can retrieve, create, read, update, and delete items.

## 🔑 Authentication

1Password SDKs support authentication with [1Password Service Accounts](https://developer.1password.com/docs/service-accounts/get-started/). You can create service accounts if you're an owner or administrator on your team. Otherwise, ask your administrator for a service account token.

Before you get started, [create a service account](https://developer.1password.com/docs/service-accounts/get-started/#create-a-service-account) and give it the appropriate permissions in the vaults where the items you want to use with the SDK are saved.

## ❗ Limitations

1Password SDKs currently only support operations on text and concealed fields. If you update or delete an item that has information saved in other field types, that information will be permanently lost.

1Password SDKs don't yet support using secret references with query parameters, so you can't retrieve file attachments or SSH keys, or get more information about field metadata.

When managing items with 1Password SDKs, you must use [unique identifiers (IDs)](https://developer.1password.com/docs/sdks/concepts#unique-identifiers-ids) in place of vault, item, and field names.

## 🚀 Get started

To use the 1Password Python SDK in your project:

1. Provision your [service account](#authentication) token. We recommend provisioning your token from the environment. For example, to export your token to the `OP_SERVICE_ACCOUNT_TOKEN` environment variable:
    
    **Mac**
    
    ```bash
    export OP_SERVICE_ACCOUNT_TOKEN=<your-service-account-token>
    ```
    
    **Windows**
    
    ```powershell
    $Env:OP_SERVICE_ACCOUNT_TOKEN = "<your-service-account-token>"
    ```

2. Install the 1Password Python SDK in your project:

    ```bash
    pip install git+ssh://git@github.com/1Password/onepassword-sdk-python.git
    ```

3. Import the SDK in your project:

    ```python
    from onepassword.client import Client
    ```

5. Initialize the SDK. Provision your service account token and use `integration_name` and `integration_version` to specify a name and version for your application.

    ```python
    async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    
    # Connects to 1Password.
    client = await Client.authenticate(auth=token, integration_name="My 1Password Integration", integration_version="v1.0.0")
    ```

### Example

```python
import asyncio
import os
from onepassword.client import Client

async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    
    # Connects to 1Password.
    client = await Client.authenticate(auth=token, integration_name="My 1Password Integration", integration_version="v1.0.0")
   
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    print(value)

if __name__ == '__main__':
    asyncio.run(main())

```

Make sure to use [secret reference URIs](https://developer.1password.com/docs/cli/secret-reference-syntax/) with the syntax `op://vault/item/field` to securely load secrets from 1Password into your code.

## 📖 Learn more

- [Load secrets with 1Password SDKs](https://developer.1password.com/docs/sdks/load-secrets)
- [Manage items with 1Password SDKs](https://developer.1password.com/docs/sdks/manage-items)
- [1Password SDK concepts](https://developer.1password.com/docs/sdks/concepts)


