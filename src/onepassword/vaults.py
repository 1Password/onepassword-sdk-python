# AUTO-GENERATED
from .core import _invoke
from json import loads
from .iterator import SDKIterator
from .types import VaultOverview


class Vaults:
    """
    The Vaults API holds all the operations the SDK client can perform on 1Password vaults.
    """

    def __init__(self, client_id):
        self.client_id = client_id

    async def list_all(self):
        """
        List all vaults
        """
        response = await _invoke(
            {
                "clientId": self.client_id,
                "invocation": {"name": "VaultsListAll", "parameters": {}},
            }
        )
        response_data = loads(response)

        objects = [VaultOverview(**data) for data in response_data]

        return SDKIterator(objects)
