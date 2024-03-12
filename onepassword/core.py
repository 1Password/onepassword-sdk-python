import json
import onepassword.op_uniffi_core as core

# InitClient creates a client instance in the current core module and returns its unique ID.
async def _init_client(client_config):
    return await core.init_client(json.dumps(client_config))

# Invoke calls specified business logic from core.
async def _invoke(invoke_config):
    return await core.invoke(json.dumps(invoke_config))

# ReleaseClient releases memory in the core associated with the given client ID.
def _release_client(client_id):
    return core.release_client(json.dumps(client_id))
