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
    value = await client.secrets.resolve("op://bhld6zk6hkuntyqlsjy3bdawey/Login/username")
    print(value)

    # Create an Item and add it to your vault.
    to_create = Item(
        id="",
        title="MyName",
        category="Login",
        vault_id="bhld6zk6hkuntyqlsjy3bdawey",
        fields=[
            ItemField(
                id="username",
                title="username",
                field_type="Text",
                section_id=None,
                value="mynameisjeff",
            ),
            ItemField(
                id="password",
                title="password",
                field_type="Concealed",
                section_id=None,
                value="jeff",
            ),
        ],
        sections=[ItemSection(id="", title="")],
    )
    created_item = await client.items.create(to_create)

    print(dict(created_item))

    # Retrieve an item from your vault.
    item = await client.items.get("bhld6zk6hkuntyqlsjy3bdawey", created_item.id)

    print(dict(item))

    # Update a field in your item
    item.fields[0].value = "new_value"
    updated_item = await client.items.update(item)

    print(dict(updated_item))

    # Delete a item from your vault.
    await client.items.delete("bhld6zk6hkuntyqlsjy3bdawey", updated_item.id)


if __name__ == "__main__":
    asyncio.run(main())
