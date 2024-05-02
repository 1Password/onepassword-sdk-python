from .core import _invoke
from json import loads


class Secrets:
    """Contains all operations the SDK client can perform on 1Password secrets."""

    def __init__(self, client_id):
        self.client_id = client_id

    async def resolve(self, secret_reference):
        """Resolve the secret reference to a secret."""
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
        return loads(response)
