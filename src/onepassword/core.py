import ctypes
import json
import os
import op_uniffi_core

def Invoke(invoke_config):
    return op_uniffi_core.invoke(json.dumps(invoke_config))


def InitClient(client_config):
    return op_uniffi_core.init_client(json.dumps(client_config))


def ReleaseClient(client_id):
    return op_uniffi_core.release_client(json.dumps(client_id))
