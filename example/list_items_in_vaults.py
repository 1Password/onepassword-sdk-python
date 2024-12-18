import asyncio
import os

from onepassword.client import Client

# list all items in all vaults
async def list_items_in_vaults():
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    if not token:
        raise ValueError("OP_SERVICE_ACCOUNT_TOKEN must be set.")
    client = await Client.authenticate(
        auth=token,
        # Set the following to your own integration name and version.
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )
    vaults = await client.vaults.list_all()
    async for vault in vaults:
        items = await client.items.list_all(vault.id)
        async for item in items:
            print(item.title)

if __name__ == "__main__":
    asyncio.run(list_items_in_vaults())