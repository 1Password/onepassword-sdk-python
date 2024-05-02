from .core import _invoke
import json
from .types import *


class Secrets:
    def __init__(self, client_id):
        self.client_id = client_id

    async def resolve(self, secret_reference):
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "Resolve",
                    "parameters": {
                        "secret_reference": secret_reference,
                    },
                },
            }
        )
        result = str(json.loads(response))
        return result
