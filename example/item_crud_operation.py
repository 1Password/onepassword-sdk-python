import asyncio
import os

from onepassword.client import Client
from onepassword.types import AutofillBehavior, ItemCategory, ItemCreateParams, ItemField, ItemFieldType, ItemSection, Website

# Perform CRUD operations on an item
async def item_crud_operation():
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    if not token:
        raise ValueError("OP_SERVICE_ACCOUNT_TOKEN must be set.")
    client = await Client.authenticate(
        auth=token,
        # Set the following to your own integration name and version.
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )
    # Fill in a real vault ID below
    # You can find this by using the list_vaults.py example
    # Or using `op vault list`
    vault_id = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
    to_create = ItemCreateParams(
        title="MyName",
        category=ItemCategory.LOGIN,
        vault_id=vault_id,
        fields=[
            ItemField(
                id="username",
                title="username",
                field_type=ItemFieldType.TEXT,
                value="mynameisjeff",
            ),
            ItemField(
                id="password",
                title="password",
                field_type=ItemFieldType.CONCEALED,
                value="jeff",
            ),
            ItemField(
                id="onetimepassword",
                title="one-time-password",
                field_type=ItemFieldType.TOTP,
                section_id="totpsection",
                value="otpauth://totp/my-example-otp?secret=jncrjgbdjnrncbjsr&issuer=1Password",
            ),
        ],
        sections=[
            ItemSection(id="", title=""),
            ItemSection(id="totpsection", title=""),
        ],
        tags=["test tag 1", "test tag 2"],
        websites=[
            Website(
                label="my custom website",
                url="https://example.com",
                autofill_behavior=AutofillBehavior.NEVER,
            )
        ],
    )
    created_item = await client.items.create(to_create)
    # [developer-docs.sdk.python.create-item]-end

    print(dict(created_item))

    # [developer-docs.sdk.python.resolve-totp-code]-start
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    code = await client.secrets.resolve(
        f"op://{created_item.vault_id}/{created_item.id}/TOTP_onetimepassword?attribute=totp"
    )
    print(code)
    # [developer-docs.sdk.python.resolve-totp-code]-end

    # [developer-docs.sdk.python.get-totp-item-crud]-start
    # Fetch a totp code from the item
    for f in created_item.fields:
        if f.field_type == "Totp":
            if f.details.content.error_message is not None:
                print(f.details.content.error_message)
            else:
                print(f.details.content.code)
    # [developer-docs.sdk.python.get-totp-item-crud]-end

    # [developer-docs.sdk.python.get-item]-start
    # Retrieve an item from your vault.
    item = await client.items.get(created_item.vault_id, created_item.id)
    # [developer-docs.sdk.python.get-item]-end

    print(dict(item))

    # [developer-docs.sdk.python.update-item]-start
    # Update a field in your item
    item.fields[0].value = "new_value"
    item.websites.append(
        Website(
            label="my custom website 2",
            url="https://example2.com",
            autofill_behavior=AutofillBehavior.NEVER,
        ),
    )
    updated_item = await client.items.put(item)
    # [developer-docs.sdk.python.update-item]-end

    print(dict(updated_item))
    # [developer-docs.sdk.python.delete-item]-start
    # Delete a item from your vault.
    await client.items.delete(created_item.vault_id, updated_item.id)
    # [developer-docs.sdk.python.delete-item]-end


if __name__ == "__main__":
    asyncio.run(item_crud_operation())