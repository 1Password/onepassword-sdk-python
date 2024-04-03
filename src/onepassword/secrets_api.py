from .core import _invoke

class Secrets:
    """Secrets represents all operations the SDK client can perform on 1Password secrets."""

    def __init__(self, client_id):
        self.client_id = client_id

    async def resolve(self, reference):
        """resolve returns the secret the provided reference points to."""

        response = await _invoke({
            "clientId": self.client_id,
            "invocation": {
                "name": "Resolve",
                "parameters": reference,
                }
            })
        return response
