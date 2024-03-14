import asyncio
import os
from onepassword.client import Client

async def main():
    # Gets your service account token from the OP_SERVICE_ACCOUNT_TOKEN environment variable.
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    
    # Connects to 1Password.
    client = await Client.authenticate(auth=token, integration_name="My_Project_Name", integration_version="x.x.x")
   
    # Retrieves a secret from 1Password. Takes a secret reference as input and returns the secret to which it points.
    value = await client.secrets.resolve("op://xw33qlvug6moegr3wkk5zkenoa/bckakdku7bgbnyxvqbkpehifki/foobar")
    print(value)

if __name__ == '__main__':
    asyncio.run(main())
