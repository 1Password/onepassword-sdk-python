import json
import platform

try: 
    if platform.machine() == "x86_64":
        import onepassword.lib.x86_64.op_uniffi_core as core
    elif platform.machine() == "aarch64" or platform.machine() == "arm64":
        import onepassword.lib.aarch64.op_uniffi_core as core
    else:
        raise ImportError("your machine's architecture is not currently supported: {}", platform.machine())
except OSError:
    raise ImportError("the combination of OS and architecture of your machine is not currently supported: {}", platform.platform())
    

# InitClient creates a client instance in the current core module and returns its unique ID.
async def _init_client(client_config):
    return await core.init_client(json.dumps(client_config))

# Invoke calls specified business logic from the SDK core.
async def _invoke(invoke_config):
    return await core.invoke(json.dumps(invoke_config))

# ReleaseClient releases memory in the SDK core associated with the given client ID.
def _release_client(client_id):
    return core.release_client(json.dumps(client_id))
