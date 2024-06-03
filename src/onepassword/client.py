import weakref
from .core import _init_client, _release_client
from .defaults import new_default_config
from .secrets import Secrets
from .items import Items


class Client:
    def __init__(self, client_id):
        self.secrets = Secrets(client_id)
        self.items = Items(client_id)

    @classmethod
    async def authenticate(cls, auth, integration_name, integration_version):
        config = new_default_config(
            auth=auth,
            integration_name=integration_name,
            integration_version=integration_version,
        )
        client_id = int(await _init_client(config))
        self = cls(client_id)
        self._config = config
        self._finalizer = weakref.finalize(self, _release_client, client_id)

        return self
