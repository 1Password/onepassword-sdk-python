from .core import _invoke
from json import loads


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
        return str(loads(response))
