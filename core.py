import op_sdk_core_py
import json

def Invoke(invoke_config):
    serialized_config = json.dump(invoke_config)
    secret = op_sdk_core_py.invoke(serialized_config)
    return secret

def InitClient(client_config):
    serialized_config = json.dump(client_config)
    client_id = op_sdk_core_py.init_client(serialized_config)
    return client_id

def ReleaseClient(clientID):
    op_sdk_core_py.release_client(clientID)

def allowed1PHosts():
    return (
        "*.1password.com",
        "*.1password.ca",
        "*.1password.eu",
        "*.b5staging.com",
        "*.b5dev.com",
        "*.b5dev.ca",
        "*.b5dev.eu",
        "*.b5test.com",
        "*.b5test.ca",
        "*.b5test.eu",
        "*.b5rev.com",
        "*.b5local.com",
        )