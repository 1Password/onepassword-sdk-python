import asyncio
import os
from onepassword import Client

async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    
    # Authenticates with your token and connects to 1Password.
    client = await Client.authenticate(auth=token, integration_name="My 1Password Integration", integration_version="v1.0.0")
   
    # Retrieves a secret from 1Password. 
    # Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://vault/item/field")
    print(value)

if __name__ == '__main__':
    asyncio.run(main())
