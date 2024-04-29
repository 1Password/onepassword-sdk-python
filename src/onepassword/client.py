import weakref
from .core import _init_client, _release_client
from .secrets_api import Secrets
from .defaults import new_default_config

class Client:
    """authenticate returns an authenticated client or errors if any provided information, including the SA token, is incorrect"""
    """`integration_name` represents the name of your application and `integration_version` represents the version of your application."""
    @classmethod
    async def authenticate(cls, auth, integration_name, integration_version):
        self = cls()
        self.config = new_default_config(auth=auth, integration_name=integration_name, integration_version=integration_version)
        client_id = int(await _init_client(self.config))
        self.secrets = Secrets(client_id)
        self._finalizer = weakref.finalize(self, _release_client, client_id)

        return self
