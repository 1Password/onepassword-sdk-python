import asyncio
import os
from onepassword.client import Client, DEFAULT_INTEGRATION_NAME, DEFAULT_INTEGRATION_VERSION

async def main():
    # Your service account token here
    token = os.environ("OP_SERVICE_ACCOUNT_TOKEN")
    
    # Connect to 1Password
    client = await Client.authenticate(auth=token, integration_name=DEFAULT_INTEGRATION_NAME, integration_version=DEFAULT_INTEGRATION_VERSION)
   
   # Retrieve secret from 1Password
    value = await client.secrets.resolve("op://xw33qlvug6moegr3wkk5zkenoa/bckakdku7bgbnyxvqbkpehifki/foobar")
    print(value)

if __name__ == '__main__':
    asyncio.run(main())
