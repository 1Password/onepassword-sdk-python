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

## Supported functionality

1Password SDKs are in active development. We're keen to hear what you'd like to see next. Let us know by [upvoting](https://github.com/1Password/onepassword-sdk-python/issues) or [filing](https://github.com/1Password/onepassword-sdk-python/issues/new/choose) an issue.

### Item management

Operations:

- [x] [Retrieve secrets](https://developer.1password.com/docs/sdks/load-secrets)
- [x] [Retrieve items](https://developer.1password.com/docs/sdks/manage-items#get-an-item)
- [x] [Create items](https://developer.1password.com/docs/sdks/manage-items#create-an-item)
- [x] [Update items](https://developer.1password.com/docs/sdks/manage-items#edit-an-item)
- [x] [Delete items](https://developer.1password.com/docs/sdks/manage-items#delete-an-item)
- [ ] List items
- [ ] Add & update tags on items 

Field types:
- [x] API Keys
- [x] Passwords
- [x] Concealed fields
- [x] Text fields
- [x] Notes
- [x] SSH private keys (partially supported: supported in resolving secret references, not yet supported in item create/get/update)
- [ ] SSH public keys, fingerprint and key type
- [ ] One-time passwords \
- [ ] Files attachments and Document items
- [x] URLs
- [x] Credit card number & type
- [x] Phone numbers

### Vault management
- [ ] Retrieve vaults
- [ ] Create vaults ([#36](https://github.com/1Password/onepassword-sdk-python/issues/36))
- [ ] Update vaults
- [ ] Delete vaults
- [ ] List vaults

### User & access management
- [ ] Provision users
- [ ] Retrieve users
- [ ] List users
- [ ] Suspend users
- [ ] Create groups
- [ ] Update group membership
- [ ] Update vault access & permissions

### Compliance & reporting
- [ ] Watchtower insights
- [ ] Travel mode
- [ ] Events. For now, use [1Password Events Reporting API](https://developer.1password.com/docs/events-api/) directly.

### Authentication

- [x] [1Password Service Accounts](https://developer.1password.com/docs/service-accounts/get-started/)
- [ ] User authentication
- [ ] 1Password Connect. For now, use [1Password/connect-sdk-go](https://github.com/1Password/connect-sdk-go).

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
