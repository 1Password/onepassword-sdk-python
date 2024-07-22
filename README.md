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

The 1Password Python SDK offers programmatic access to your secrets in 1Password with Python. During the beta, you can create, retrieve, update, and delete items and resolve secret references.

1Password SDKs support authentication with [1Password Service Accounts](https://developer.1password.com/docs/service-accounts/get-started/).

## Requirements

The 1Password Python SDK requires:

- `libssl` 3
- `glibc` 2.32 or later

If you're running a Linux distribution that still uses `libssl` version 1.1.1, such as Debian 11 or Ubuntu 20.04, you'll need to update to a later version of Linux or install the required dependencies.

## ❗ Limitations

1Password SDKs don't yet support using secret references to retrieve file attachments or SSH keys, or using query parameters with secret references to get more information about field and file attributes.

1Password SDKs currently only support operations on text and concealed fields. As a result, you can't edit items that include information saved in other types of fields.

When managing items with 1Password SDKs, you must use [unique identifiers (IDs)](https://developer.1password.com/docs/sdks/concepts#unique-identifiers) in place of vault, item, and field names.

## 🚀 Get started

To use the 1Password Python SDK in your project:

1. [Create a service account](https://my.1password.com/developer-tools/infrastructure-secrets/serviceaccount/) and give it the appropriate permissions in the vaults where the items you want to use with the SDK are saved.
2. Provision your service account token. We recommend provisioning your token from the environment. For example, to export your token to the `OP_SERVICE_ACCOUNT_TOKEN` environment variable:

   **macOS or Linux**

   ```bash
   export OP_SERVICE_ACCOUNT_TOKEN=<your-service-account-token>
   ```

   **Windows**

   ```powershell
   $Env:OP_SERVICE_ACCOUNT_TOKEN = "<your-service-account-token>"
   ```

3. Install the 1Password Python SDK in your project:

   ```bash
   pip install git+ssh://git@github.com/1Password/onepassword-sdk-python.git@v0.1.0-beta.9
   ```

4. Use the Python SDK in your project:

```python
import asyncio
import os
from onepassword.client import Client

async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")

    # Connects to 1Password. Fill in your own integration name and version.
    client = await Client.authenticate(auth=token, integration_name="My 1Password Integration", integration_version="v1.0.0")

    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    # use value here

if __name__ == '__main__':
    asyncio.run(main())

```

Make sure to use [secret reference URIs](https://developer.1password.com/docs/cli/secrets-reference-syntax/) with the syntax `op://vault/item/field` to securely load secrets from 1Password into your code.

## 📖 Learn more

- [Load secrets with 1Password SDKs](https://developer.1password.com/docs/sdks/load-secrets)
- [Manage items with 1Password SDKs](https://developer.1password.com/docs/sdks/manage-items)
- [1Password SDK concepts](https://developer.1password.com/docs/sdks/concepts)
