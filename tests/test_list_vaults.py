import asyncio
import os

from onepassword.client import Client

async def test_list_vaults():
    print("Starting list_vaults test")
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
        print(vault.title)
    
    print("Finished list_vaults test successfully")

if __name__ == "__main__":
    asyncio.run(test_list_vaults())