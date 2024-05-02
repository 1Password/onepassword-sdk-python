import asyncio
import os
from onepassword.client import Client
from onepassword.types import *

async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")

    # Connects to 1Password.
    client = await Client.authenticate(
        auth=token,
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    print(value)

    # Create an Item and add it to your vault.
    created_item = Item(id="",title="MyName",category="Login",vault_id="vault_id",fields=[ItemField(id="username",title="username",field_type="Text", section_id=None,value="mynameisjeff"),ItemField(id="password",title="password",field_type="Concealed",section_id=None,value="jeff")],sections=[ItemSection(id="",title="")])

    # Retrieve an item from your vault. 
    item = await client.items.get("vault_id","item_id")
    
    # Update a field in your item
    item.fields[0].value = "new_value"

    updated_item = await client.items.update(item)

    # Delete a item from your vault.
    await client.items.delete("vault_id","item_id")

if __name__ == "__main__":
    asyncio.run(main())
