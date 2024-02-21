import ctypes
import json
import os

lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "../../python-sdk-core/libop_uniffi_core.dylib"))

def Invoke(invoke_config):

    invoke = lib.uniffi_op_uniffi_core_fn_func_invoke
    invoke.restype = ctypes.c_int
    invoke.argtypes = [ctypes.c_wchar_p]

    return invoke(json.dumps(invoke_config))


def InitClient(client_config):
    init_client = lib.uniffi_op_uniffi_core_fn_func_init_client
    init_client.restype = ctypes.c_int
    init_client.argtypes = [ctypes.c_wchar_p]

    return init_client(json.dumps(client_config))


def ReleaseClient(client_id):
    release_client = lib.uniffi_op_uniffi_core_fn_func_release_client
    release_client.restype = ctypes.c_int  # possibly void? return type is Rust Result ()
    release_client.argtypes = [ctypes.c_wchar_p]
    
    return release_client(json.dumps(client_id))

# sample code below for reference

# lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "../python-sdk-core/libop_uniffi_core.dylib"))
# lib.invoke.restype = ctypes.c_char_p  # declare function invoke and declare function's return type
# lib.invoke.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]  # declare function parameters

# returned_err = ctypes.c_int(0)
# id = ctypes.c_long(invoke_config.clientId)
# arg_arr = json.dumps(invoke_config)
# result = lib.invoke(id, method.encode("utf-8"), arg_arr, returned_err)
# if returned_err.value == 1:
#     raise Exception(result)
# else:
#     return result
