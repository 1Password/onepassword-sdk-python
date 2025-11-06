import json
import platform
from typing import Protocol
from onepassword.desktop_core import DesktopCore
from onepassword.errors import raise_typed_exception, DesktopSessionExpired

# In empirical tests, we determined that maximum message size that can cross the FFI boundary
# is ~128MB. Past this limit, FFI will throw an error and the program will crash.
# We set the limit to 50MB to be safe and consistent with the other SDKs (where this limit is 64MB), to be reconsidered upon further testing
MESSAGE_LIMIT = 50 * 1024 * 1024


class Core(Protocol):
    async def init_client(self, client_config: dict) -> str: ...
    async def invoke(self, invoke_config: dict) -> str: ...
    def invoke_sync(self, invoke_config: dict) -> str: ...
    def release_client(self, client_id: int) -> None: ...


class InnerClient:
    client_id: int
    core: DesktopCore | UniffiCore
    config: dict[str, any]

    def __init__(self, client_id: int, core: "DesktopCore | UniffiCore", config: dict[str, any]):
        self.client_id = client_id
        self.core = core
        self.config = config

    async def invoke(self, invoke_config: dict):
        try:
            return await self.core.invoke(invoke_config)
        except DesktopSessionExpired as e:
            new_client_id = await self.core.init_client(self.config)
            self.client_id = new_client_id
            invoke_config["invocation"]["clientId"] = self.client_id
            return await self.core.invoke(invoke_config)
        except Exception as e:
            raise e


class UniffiCore:
    def __init__(self):
        machine_arch = platform.machine().lower()

        if machine_arch in ["x86_64", "amd64"]:
            import onepassword.lib.x86_64.op_uniffi_core as core
        elif machine_arch in ["aarch64", "arm64"]:
            import onepassword.lib.aarch64.op_uniffi_core as core
        else:
            raise ImportError(
                f"Your machine's architecture is not currently supported: {machine_arch}"
            )

        self.core = core

    async def init_client(self, client_config: dict):
        """Creates a client instance in the current core module and returns its unique ID."""
        try:
            return await self.core.init_client(json.dumps(client_config))
        except Exception as e:
            raise_typed_exception(e)

    async def invoke(self, invoke_config: dict):
        """Invoke business logic asynchronously."""
        serialized_config = json.dumps(invoke_config)
        if len(serialized_config.encode()) > MESSAGE_LIMIT:
            raise ValueError(
                f"message size exceeds the limit of {MESSAGE_LIMIT} bytes, "
                "please contact 1Password at support@1password.com or "
                "https://developer.1password.com/joinslack if you need help."
            )
        try:
            return await self.core.invoke(serialized_config)
        except Exception as e:
            raise_typed_exception(e)

    def invoke_sync(self, invoke_config: dict):
        """Invoke business logic synchronously."""
        serialized_config = json.dumps(invoke_config)
        if len(serialized_config.encode()) > MESSAGE_LIMIT:
            raise ValueError(
                f"message size exceeds the limit of {MESSAGE_LIMIT} bytes, "
                "please contact 1Password at support@1password.com or "
                "https://developer.1password.com/joinslack if you need help."
            )
        try:
            return self.core.invoke_sync(serialized_config)
        except Exception as e:
            raise_typed_exception(e)

    def release_client(self, client_id: int):
        """Releases memory in the SDK core associated with the given client ID."""
        try:
            return self.core.release_client(json.dumps(client_id))
        except Exception as e:
            raise_typed_exception(e)
