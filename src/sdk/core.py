# omitting op_sdk_core_py.so import and shared library calls for the time being
# should be added back when we start work on the core

#import op_sdk_core_py
import json


def Invoke(invoke_config):
    serialized_config = json.dump(invoke_config)
    #secret = op_sdk_core_py.invoke(serialized_config)
    #return secret


def InitClient(client_config):
    serialized_config = json.dump(client_config)
    #client_id = op_sdk_core_py.init_client(serialized_config)
    #return client_id


def ReleaseClient(clientID):
    #op_sdk_core_py.release_client(clientID)
    pass
