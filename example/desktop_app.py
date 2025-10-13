# [developer-docs.sdk.python.sdk-import]-start
from onepassword import *
import asyncio


async def main():
    # [developer-docs.sdk.python.client-initialization]-start
    # Connects to the 1Password desktop app.
    client = await Client.authenticate(
        auth=DesktopAuth(
            account_name="AndiTituTest"  # Set to your 1Password account name.
        ),
        # Set the following to your own integration name and version.
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )
    
    # [developer-docs.sdk.python.list-vaults]-start
    vaults = await client.vaults.list()
    for vault in vaults:
        print(vault)
    # [developer-docs.sdk.python.list-vaults]-end

    # [developer-docs.sdk.python.list-items]-start
    overviews = await client.items.list("xw33qlvug6moegr3wkk5zkenoa")
    for overview in overviews:
        print(overview.title)
    # [developer-docs.sdk.python.list-items]-end


if __name__ == "__main__":
    asyncio.run(main())