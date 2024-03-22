import asyncio
import os
from onepassword.client import Client, DEFAULT_INTEGRATION_NAME, DEFAULT_INTEGRATION_VERSION

async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    
    # Connects to 1Password.
    client = await Client.authenticate(auth=token, integration_name=DEFAULT_INTEGRATION_NAME, integration_version=DEFAULT_INTEGRATION_VERSION)
   
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    print(value)

if __name__ == '__main__':
    asyncio.run(main())
