<p align="center">
  <a href="https://1password.com">
      <h1 align="center">1Password Python SDK</h1>
  </a>
</p>

<p align="center">
 <h4 align="center">Build integrations that programmatically interact with 1Password.</h4>
</p>

<p align="center">
  <a href="https://developer.1password.com/docs/sdks/">Documentation</a> | <a href="https://github.com/1Password/onepassword-sdk-python/tree/main/example">Examples</a>
<br/>

---

## Requirements

The 1Password Python SDK is compatible with:

- `python` 3.9 or later
- `libssl` 3
- `glibc` 2.32 or later

If you're running a Linux distribution that still uses `libssl` version 1.1.1, such as Debian 11 or Ubuntu 20.04, you'll need to update to a later version of Linux or install the required dependencies.

## 🚀 Get started

You can choose between two [authentication methods](https://developer.1password.com/docs/sdks/concepts#authentication) for the 1Password Python SDK: local authorization prompts from the [1Password desktop app](#option-1-1password-desktop-app) or automated authentication with a [1Password Service Account](#option-2-1password-service-account).

### Option 1: 1Password desktop app

[1Password desktop app authentication](https://developer.1password.com/docs/sdks/concepts#1password-desktop-app) is best for local integrations that require minimal setup from end users and sensitive workflows that require human-in-the-loop approval. To set up the SDK to authenticate with the 1Password app:

1. Install the [1Password desktop app](https://1password.com/downloads/) and sign in to your account in the app.
2. Select your account or collection at the top of the sidebar, then navigate to **Settings** > **Developer**.
3. Under Integrate with the 1Password SDKs, select **Integrate with other apps**.
4. If you want to authenticate with biometrics, navigate to **Settings** > **Security**, then turn on the option to unlock using [Touch ID](https://support.1password.com/touch-id-mac/),  [Windows Hello](https://support.1password.com/windows-hello/), or [system authentication](https://support.1password.com/system-authentication-linux/).
5. Install the 1Password Python SDK in your project:

   ```bash
   pip install onepassword-sdk
   ```

6. To use the Python SDK in your project, replace `your-account-name` in the code below with the name of your 1Password account as it appears at the top left sidebar of the 1Password desktop app.

```python
import asyncio
import os
from onepassword.client import Client, DesktopAuth

async def main():
    # Connects to 1Password. Fill in your own integration name and version.
    client = await Client.authenticate(
    auth=DesktopAuth(
        # TODO: Set to your 1Password account name.
        account_name="your-account-name"
    ),
    # TODO: Set to your own integration name and version.
    integration_name="My 1Password Integration",
    integration_version="v1.0.0",
)

    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    # use value here

if __name__ == '__main__':
    asyncio.run(main())

```

Make sure to use [secret reference URIs](https://developer.1password.com/docs/cli/secret-reference-syntax/) with the syntax `op://vault/item/field` to securely load secrets from 1Password into your code.

### Option 2: 1Password Service Account

[Service account authentication](https://developer.1password.com/docs/sdks/concepts/#1password-service-account) is best for automated access and limiting your integration to least privilege access. To set up the SDK to authenticate with a service account token:

1. [Create a service account](https://my.1password.com/developer-tools/infrastructure-secrets/serviceaccount/?source=github-sdk) and give it the appropriate permissions in the vaults where the items you want to use with the SDK are saved.
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
   pip install onepassword-sdk
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

Make sure to use [secret reference URIs](https://developer.1password.com/docs/cli/secret-reference-syntax/) with the syntax `op://vault/item/field` to securely load secrets from 1Password into your code.

## Supported functionality

1Password SDKs are in active development. We're keen to hear what you'd like to see next. Let us know by [upvoting](https://github.com/1Password/onepassword-sdk-python/issues) or [filing](https://github.com/1Password/onepassword-sdk-python/issues/new/choose) an issue.

### Item management

**Operations:**

- [x] [Retrieve secrets](https://developer.1password.com/docs/sdks/load-secrets)
- [x] [Retrieve items](https://developer.1password.com/docs/sdks/manage-items#get-an-item)
- [x] [Create items](https://developer.1password.com/docs/sdks/manage-items#create-an-item)
- [x] [Update items](https://developer.1password.com/docs/sdks/manage-items#update-an-item)
- [x] [Delete items](https://developer.1password.com/docs/sdks/manage-items#delete-an-item)
- [x] [Archive items](https://developer.1password.com/docs/sdks/manage-items/#archive-an-item)
- [x] [List items](https://developer.1password.com/docs/sdks/list-vaults-items/)
- [x] [Share items](https://developer.1password.com/docs/sdks/share-items)
- [x] [Generate PIN, random and memorable passwords](https://developer.1password.com/docs/sdks/manage-items#generate-a-password)

**Field types:**

- [x] API Keys
- [x] Passwords
- [x] Concealed fields
- [x] Text fields
- [x] Notes
- [x] SSH private keys, public keys, fingerprint and key type
- [x] One-time passwords
- [x] URLs
- [x] Websites (used to suggest and autofill logins)
- [x] Phone numbers
- [x] Credit card types
- [x] Credit card numbers
- [x] Emails
- [x] References to other items
- [x] Address
- [x] Date
- [x] MM/YY
- [x] File attachments and Document items
- [x] Menu
- [ ] Passkeys

### Vault management

- [x] [Retrieve vaults](https://developer.1password.com/docs/sdks/vaults#get-a-vault-overview)
- [x] [Create vaults](https://developer.1password.com/docs/sdks/vaults#create-a-vault)
- [x] [Update vaults](https://developer.1password.com/docs/sdks/vaults#update-a-vault)
- [x] [Delete vaults](https://developer.1password.com/docs/sdks/vaults#delete-a-vault)
- [x] [List vaults](https://developer.1password.com/docs/sdks/list-vaults-items#list-vaults)
- [x] [Manage group vault permissions](https://developer.1password.com/docs/sdks/vault-permissions)
- [ ] Manage user vault permissions

### User & access management

- [ ] Provision users
- [ ] Retrieve users
- [ ] List users
- [ ] Suspend users
- [x] [Retrieve groups](https://developer.1password.com/docs/sdks/groups/)
- [ ] List groups
- [ ] Create groups
- [ ] Update group membership

## Environments management

- [x] [Read 1Password Environments](https://developer.1password.com/docs/sdks/environments) (beta)

### Compliance & reporting

- [ ] Watchtower insights
- [ ] Travel mode
- [ ] Events. For now, use [1Password Events Reporting API](https://developer.1password.com/docs/events-api/) directly.

### Authentication

- [x] [1Password Service Accounts](https://developer.1password.com/docs/sdks/concepts#1password-service-account)
- [x] [User authentication](https://developer.1password.com/docs/sdks/concepts#1password-desktop-app)
- [ ] 1Password Connect. For now, use [1Password/connect-sdk-python](https://github.com/1Password/connect-sdk-python).

## 📖 Learn more

- [Load secrets](https://developer.1password.com/docs/sdks/load-secrets)
- [Read 1Password Environments (beta)](https://developer.1password.com/docs/sdks/environments)
- [Manage items](https://developer.1password.com/docs/sdks/manage-items)
- [Manage files](https://developer.1password.com/docs/sdks/files)
- [Share items](https://developer.1password.com/docs/sdks/share-items)
- [List vaults and items](https://developer.1password.com/docs/sdks/list-vaults-items)
- [Manage vaults](https://developer.1password.com/docs/sdks/vaults)
- [Manage vault permissions](https://developer.1password.com/docs/sdks/vault-permissions)
- [Manage groups](https://developer.1password.com/docs/sdks/groups)
- [1Password SDK concepts](https://developer.1password.com/docs/sdks/concepts)
