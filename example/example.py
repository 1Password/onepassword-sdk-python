import asyncio
import os
from pathlib import Path

# [developer-docs.sdk.python.sdk-import]-start
from onepassword import *

# [developer-docs.sdk.python.sdk-import]-end
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


async def main():
    # [developer-docs.sdk.python.client-initialization]-start
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")

    # Connects to 1Password.
    client = await Client.authenticate(
        auth="AgHouUoF1O06H1z9hJjQofEveT3ITHGYmTEvCucRNtokepcEC7vLiq5L95Dc42Fwljzj5tsqWRujsUHOkyuLPOnn_BrJu0H81x2CBKnerwMdlgc",
        # Set the following to your own integration name and version.
        integration_name="My 1Password Integration",
        integration_version="v1.0.0",
    )
    # [developer-docs.sdk.python.client-initialization]-end

    secret = await client.items.get("54jd5fopcp34u2rqqypee6uofm", "it76yngyalveqbmbbz4ijhwnrq")
    print(f"Secret resolved: {secret}")

if __name__ == "__main__":
    asyncio.run(main())

