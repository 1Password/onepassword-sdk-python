import asyncio
import os

# [developer-docs.sdk.python.sdk-import]-start
from onepassword import *
# [developer-docs.sdk.python.sdk-import]-end


async def main():
    # [developer-docs.sdk.python.client-initialization]-start
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")

    # Connects to 1Password.
    client = await Client.authenticate(
        auth=token,
        # Set the following to your own integration name and version.
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )
    # [developer-docs.sdk.python.client-initialization]-end

    # [developer-docs.sdk.python.list-vaults]-start
    vaults = await client.vaults.list_all()
    async for vault in vaults:
        print(vault.title)
    # [developer-docs.sdk.python.list-vaults]-end

    # [developer-docs.sdk.python.list-items]-start
    items = await client.items.list_all(vault.id)
    async for item in items:
        print(item.title)
    # [developer-docs.sdk.python.list-items]-end

    # [developer-docs.sdk.python.validate-secret-reference]-start
    # Validate secret reference to ensure no syntax errors
    try:
        await Secrets.validate_secret_reference("op//vault/item/field")
    except Exception as error:
        print(error)
    # [developer-docs.sdk.python.validate-secret-reference]-end

    # [developer-docs.sdk.python.resolve-secret]-start
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    print(value)
    # [developer-docs.sdk.python.resolve-secret]-end

    # [developer-docs.sdk.python.create-item]-start
    # Create an Item and add it to your vault.
    to_create = ItemCreateParams(
        title="MyName",
        category="Login",
        vault_id="q73bqltug6xoegr3wkk2zkenoq",
        fields=[
            ItemField(
                id="username",
                title="username",
                field_type="Text",
                value="mynameisjeff",
            ),
            ItemField(
                id="password",
                title="password",
                field_type="Concealed",
                value="jeff",
            ),
            ItemField(
                id="onetimepassword",
                title="one-time-password",
                field_type="Totp",
                section_id="totpsection",
                value="otpauth://totp/my-example-otp?secret=jncrjgbdjnrncbjsr&issuer=1Password",
            ),
        ],
        sections=[
            ItemSection(id="", title=""),
            ItemSection(id="totpsection", title=""),
        ],
        tags=["test tag 1", "test tag 2"]
    )
    created_item = await client.items.create(to_create)
    # [developer-docs.sdk.python.create-item]-end

    print(dict(created_item))

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
    updated_item = await client.items.put(item)
    # [developer-docs.sdk.python.update-item]-end

    print(dict(updated_item))
    # [developer-docs.sdk.python.delete-item]-start
    # Delete a item from your vault.
    await client.items.delete(created_item.vault_id, updated_item.id)
    # [developer-docs.sdk.python.delete-item]-end


if __name__ == "__main__":
    asyncio.run(main())
