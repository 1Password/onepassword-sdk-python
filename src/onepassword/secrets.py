from .core import _invoke

"""Secrets represents all operations the SDK client can perform on 1Password secrets."""


class Secrets:
    def __init__(self, client_id):
        self.client_id = client_id

    """resolve returns the secret the provided reference points to."""

    async def resolve(self, reference):
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "Resolve",
                    "parameters": {
                        "secret_reference": reference,
                    },
                },
            }
        )
        return response
