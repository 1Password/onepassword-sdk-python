import json
import op_uniffi_core


async def InitClient(client_config):
    return await op_uniffi_core.init_client(json.dumps(client_config))


async def Invoke(invoke_config):
    return await op_uniffi_core.invoke(json.dumps(invoke_config))


def ReleaseClient(client_id):
    return op_uniffi_core.release_client(json.dumps(client_id))
