# AUTO-GENERATED
from typing import Optional
import weakref
from .core import _init_client, _release_client
from .defaults import new_default_config
from .secrets import Secrets
from .items import Items
from .vaults import Vaults


class Client:
    secrets: Secrets
    items: Items
    vaults: Vaults

    @classmethod
    async def authenticate(cls, auth: Optional[str], integration_name, integration_version):
        # Convert None from os.getEnv to empty string
        config = new_default_config(
            auth=auth or "",
            integration_name=integration_name,
            integration_version=integration_version,
        )
        client_id = int(await _init_client(config))

        authenticated_client = cls()

        authenticated_client.secrets = Secrets(client_id)
        authenticated_client.items = Items(client_id)
        authenticated_client.vaults = Vaults(client_id)
        authenticated_client._finalizer = weakref.finalize(
            cls, _release_client, client_id
        )

        return authenticated_client
