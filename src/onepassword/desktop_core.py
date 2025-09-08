import ctypes
import json
import os
import platform
import sys
from ctypes import c_uint8, c_size_t, c_int32, POINTER, byref, c_void_p
from .core import UniffiCore


def find_1password_lib_path():
    host_os = platform.system().lower()  # "darwin", "linux", "windows"

    core = UniffiCore()
    if core is None:
        raise RuntimeError("failed to get ExtismCore")

    locations_raw = core.invoke({
        "invocation": {
            "parameters": {
                "methodName": "GetDesktopAppIPCClientLocations",
                "serializedParams": {"host_os": host_os},
            }
        }
    })

    try:
        locations = json.loads(locations_raw)
    except Exception as e:
        raise RuntimeError(f"failed to parse core response: {e}")

    for lib_path in locations:
        if os.path.exists(lib_path):
            return lib_path

    raise FileNotFoundError("1Password desktop application not found")

class DesktopCore:
    def __init__(self):
        # Determine the path to the desktop app.
        path = find_1password_lib_path()

        self.lib = ctypes.CDLL(path)

        # Bind the Rust-exported functions
        self.send_message = self.lib.op_sdk_ipc_send_message
        self.send_message.argtypes = [
            POINTER(c_uint8),             # msg_ptr
            c_size_t,                     # msg_len
            POINTER(POINTER(c_uint8)),    # out_buf
            POINTER(c_size_t),            # out_len
            POINTER(c_size_t),            # out_cap
        ]
        self.send_message.restype = c_int32

        self.free_message = self.lib.op_sdk_ipc_free_response
        self.free_message.argtypes = [POINTER(c_uint8), c_size_t, c_size_t]
        self.free_message.restype = None

    def call_shared_library(self, payload: bytes) -> bytes:
        out_buf = POINTER(c_uint8)()
        out_len = c_size_t()
        out_cap = c_size_t()

        ret = self.send_message(
            (ctypes.cast(payload, POINTER(c_uint8))),
            len(payload),
            byref(out_buf),
            byref(out_len),
            byref(out_cap),
        )

        if ret != 0:
            raise RuntimeError(f"send_message failed with code {ret}")

        # Copy bytes into Python
        data = ctypes.string_at(out_buf, out_len.value)

        # Free memory via Rust's exported function
        self.free_message(out_buf, out_len, out_cap)

        return data

    def init_client(self, config: dict) -> int:
        payload = json.dumps(config).encode("utf-8")
        resp = self.call_shared_library(payload)
        return json.loads(resp)

    def invoke(self, invoke_config: dict) -> str:
        payload = json.dumps(invoke_config).encode("utf-8")
        resp = self.call_shared_library(payload)
        return resp.decode("utf-8")

    def release_client(self, client_id: int):
        payload = json.dumps(client_id).encode("utf-8")
        try:
            self.call_shared_library(payload)
        except Exception as e:
            print(f"failed to release client: {e}")
