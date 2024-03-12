import json
import sys
import importlib.util
#import op_uniffi_lib_mac_arm64.op_uniffi_core as core

if (spec := importlib.util.find_spec("op_uniffi_lib_mac_arm64.op_uniffi_core")) is not None:
    module = importlib.util.module_from_spec(spec)
    print(module)
    sys.modules["core"] = module
    spec.loader.exec_module(module)
    print(f"op_uniffi_lib_mac_arm64 has been imported")
elif (spec := importlib.util.find_spec("op_uniffi_lib_linux_amd64")) is not None:
    module = importlib.util.module_from_spec(spec)
    sys.modules["core"] = module
    spec.loader.exec_module(module)

core = sys.modules["core"]

# InitClient creates a client instance in the current core module and returns its unique ID.
async def _init_client(client_config):
    return await core.init_client(json.dumps(client_config))

# Invoke calls specified business logic from core.
async def _invoke(invoke_config):
    return await core.invoke(json.dumps(invoke_config))

# ReleaseClient releases memory in the core associated with the given client ID.
def _release_client(client_id):
    return core.release_client(json.dumps(client_id))
