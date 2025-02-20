import json
import platform

from onepassword.errors import raise_typed_exception


machine_arch = platform.machine().lower()

if machine_arch in ["x86_64", "amd64"]:
    import onepassword.lib.x86_64.op_uniffi_core as core
elif machine_arch in ["aarch64", "arm64"]:
    import onepassword.lib.aarch64.op_uniffi_core as core
else:
    raise ImportError(
        f"Your machine's architecture is not currently supported: {machine_arch}"
    )


# InitClient creates a client instance in the current core module and returns its unique ID.
async def _init_client(client_config):
    try:
        return await core.init_client(json.dumps(client_config))
    except Exception as e:
        raise_typed_exception(e)


# Invoke calls specified business logic from the SDK core.
async def _invoke(invoke_config):
    try:
        return await core.invoke(json.dumps(invoke_config))
    except Exception as e:
        raise_typed_exception(e)


# Invoke calls specified business logic from the SDK core.
def _invoke_sync(invoke_config):
    try:
        return core.invoke_sync(json.dumps(invoke_config))
    except Exception as e:
        raise_typed_exception(e)


# ReleaseClient releases memory in the SDK core associated with the given client ID.
def _release_client(client_id):
    return core.release_client(json.dumps(client_id))
