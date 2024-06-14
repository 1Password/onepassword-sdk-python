import weakref
from .core import _init_client, _release_client
from .defaults import new_default_config
from .secrets import Secrets
from .items import Items


class Client:
    @classmethod
    async def authenticate(cls, auth, integration_name, integration_version):
        self = cls()

        self.config = new_default_config(
            auth=auth,
            integration_name=integration_name,
            integration_version=integration_version,
        )
        client_id = int(await _init_client(self.config))

        self.secrets = Secrets(client_id)
        self.items = Items(client_id)
        self._finalizer = weakref.finalize(self, _release_client, client_id)

        return self
