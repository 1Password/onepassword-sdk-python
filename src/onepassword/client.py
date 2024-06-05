# AUTO-GENERATED
import weakref
from .core import _init_client, _release_client
from .defaults import new_default_config
from .secrets import Secrets
from .items import Items


class Client:
    secrets: Secrets
    items: Items

    @classmethod
    async def authenticate(self, auth, integration_name, integration_version):
        config = new_default_config(
            auth=auth,
            integration_name=integration_name,
            integration_version=integration_version,
        )
        client_id = int(await _init_client(config))

        authenticated_client = self()

        authenticated_client.secrets = Secrets(client_id)
        authenticated_client.items = Items(client_id)
        authenticated_client._finalizer = weakref.finalize(self, _release_client, client_id)

        return authenticated_client
