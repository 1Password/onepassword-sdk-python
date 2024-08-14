# AUTO-GENERATED
from .core import _invoke
from json import loads
from .iterator import SDKIterator


class Secrets:
    """
    The Secrets API includes all operations the SDK client can perform on secrets.
    Use secret reference URIs to securely load secrets from 1Password: op://<vault-name>/<item-name>[/<section-name>]/<field-name>
    """

    def __init__(self, client_id):
        self.client_id = client_id

    async def resolve(self, secret_reference):
        """
        Resolve returns the secret the provided secret reference points to.
        """
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {
                    "name": "SecretsResolve",
                    "parameters": {
                        "secret_reference": secret_reference,
                    },
                },
            }
        )
        return str(loads(response))
