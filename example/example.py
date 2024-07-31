import asyncio
import os
from onepassword import *


async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")

    # Connects to 1Password.
    client = await Client.authenticate(
        auth=token,
        # Set the following to your own integration name and version.
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )

    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    print(value)

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
                section_id=None,
                value="mynameisjeff",
                details=None,
            ),
            ItemField(
                id="password",
                title="password",
                field_type="Concealed",
                section_id=None,
                value="jeff",
                details=None,
            ),
            ItemField(
                id="onetimepassword",
                title="one-time-password",
                field_type="Totp",
                section_id="totpsection",
                value="otpauth://totp/my-example-otp?secret=jncrjgbdjnrncbjsr&issuer=1Password",
                details=None,
            ),
        ],
        sections=[
            ItemSection(id="", title=""),
            ItemSection(id="totpsection", title=""),
        ],
    )
    created_item = await client.items.create(to_create)

    print(dict(created_item))

    # Fetch a totp code from the item
    for f in created_item.fields:
        if f.field_type == "Totp":
            if f.details.content.error_message is not None:
                print(f.details.content.error_message)
            else:
                print(f.details.content.code)

    # Retrieve an item from your vault.
    item = await client.items.get(created_item.vault_id, created_item.id)

    print(dict(item))

    # Update a field in your item
    item.fields[0].value = "new_value"
    updated_item = await client.items.put(item)

    print(dict(updated_item))

    # Delete a item from your vault.
    await client.items.delete(created_item.vault_id, updated_item.id)


if __name__ == "__main__":
    asyncio.run(main())
