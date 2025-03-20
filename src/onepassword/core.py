import json
import platform

from onepassword.errors import raise_typed_exception

# In empirical tests, we determined that maximum message size that can cross the FFI boundary
# is ~128MB. Past this limit, FFI will throw an error and the program will crash.
# We set the limit to 50MB to be safe and consistent with the other SDKs (where this limit is 64MB), to be reconsidered upon further testing
MESSAGE_LIMIT = 50 * 1024 * 1024

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
    serialized_config = json.dumps(invoke_config)
    if len(serialized_config.encode()) > MESSAGE_LIMIT:
        raise ValueError(
            f"message size exceeds the limit of {MESSAGE_LIMIT} bytes, please contact 1Password at support@1password.com or https://developer.1password.com/joinslack if you need help."
        )
    try:
        return await core.invoke(serialized_config)
    except Exception as e:
        raise_typed_exception(e)


# Invoke calls specified business logic from the SDK core.
def _invoke_sync(invoke_config):
    serialized_config = json.dumps(invoke_config)
    if len(serialized_config.encode()) > MESSAGE_LIMIT:
        raise ValueError(
            f"message size exceeds the limit of {MESSAGE_LIMIT} bytes, please contact 1Password at support@1password.com or https://developer.1password.com/joinslack if you need help."
        )
    try:
        return core.invoke_sync(serialized_config)
    except Exception as e:
        raise_typed_exception(e)


# ReleaseClient releases memory in the SDK core associated with the given client ID.
def _release_client(client_id):
    return core.release_client(json.dumps(client_id))
