import json
import importlib.util

def import_core(platform_specific_package):
    if (spec := importlib.util.find_spec(platform_specific_package)) is not None:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None

potential_dependencies = [
    "sdk_core_linux_amd64.op_uniffi_core",
    "sdk_core_mac_arm64.op_uniffi_core"
]

core = None

for dep in potential_dependencies:
    try: 
        core = import_core(dep)
        if core is not None:
            break
    except ModuleNotFoundError:
        continue



# InitClient creates a client instance in the current core module and returns its unique ID.
async def _init_client(client_config):
    return await core.init_client(json.dumps(client_config))

# Invoke calls specified business logic from core.
async def _invoke(invoke_config):
    return await core.invoke(json.dumps(invoke_config))

# ReleaseClient releases memory in the core associated with the given client ID.
def _release_client(client_id):
    return core.release_client(json.dumps(client_id))
