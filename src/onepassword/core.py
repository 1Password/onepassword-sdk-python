import json
import op_uniffi_core

# InitClient creates a client instance in the current core module and returns its unique ID.
async def InitClient(client_config):
    return await op_uniffi_core.init_client(json.dumps(client_config))

# Invoke calls specified business logic from core.
async def Invoke(invoke_config):
    return await op_uniffi_core.invoke(json.dumps(invoke_config))

# ReleaseClient releases memory in the core associated with the given client ID.
def ReleaseClient(client_id):
    return op_uniffi_core.release_client(json.dumps(client_id))
