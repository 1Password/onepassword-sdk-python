from .core import _invoke
import json
from .types import *


class Items:
    def __init__(self, client_id):
        self.client_id = client_id

    async def create(self, item):
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "Create",
                    "parameters": {
                        "item": item,
                    },
                },
            }
        )
        result = Item(**json.loads(response))
        return result


async def get(self, vault_id, item_id):
    response = await _invoke(
        {
            "clientId": self.client_id,
            "invocation": {
                "name": "Get",
                "parameters": {
                    "vault_id": vault_id,
                    "item_id": item_id,
                },
            },
        }
    )
    result = Item(**json.loads(response))
    return result


async def update(self, item):
    response = await _invoke(
        {
            "clientId": self.client_id,
            "invocation": {
                "name": "Update",
                "parameters": {
                    "item": item,
                },
            },
        }
    )
    result = Item(**json.loads(response))
    return result


async def delete(self, vault_id, item_id):
    await _invoke(
        {
            "clientId": self.client_id,
            "invocation": {
                "name": "Delete",
                "parameters": {
                    "vault_id": vault_id,
                    "item_id": item_id,
                },
            },
        }
    )
