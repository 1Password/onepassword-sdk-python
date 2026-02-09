import ctypes
import json
import os
import platform
import base64
from pathlib import Path
import sys
from ctypes import c_uint8, c_size_t, c_int32, POINTER, byref
from onepassword.errors import raise_typed_exception


def find_1password_lib_path():
    os_name = platform.system()

    # Define paths based on OS
    if os_name == "Darwin":  # macOS
        locations = [
            "/Applications/1Password.app/Contents/Frameworks/libop_sdk_ipc_client.dylib",
            str(
                Path.home()
                / "Applications/1Password.app/Contents/Frameworks/libop_sdk_ipc_client.dylib"
            ),
        ]
    elif os_name == "Linux":
        locations = [
            "/usr/bin/1password/libop_sdk_ipc_client.so",
            "/opt/1Password/libop_sdk_ipc_client.so",
            "/snap/bin/1password/libop_sdk_ipc_client.so",
        ]
    elif os_name == "Windows":
        locations = [
            str(Path.home() / r"AppData\Local\1Password\op_sdk_ipc_client.dll"),
            r"C:\Program Files\1Password\app\8\op_sdk_ipc_client.dll",
            r"C:\Program Files (x86)\1Password\app\8\op_sdk_ipc_client.dll",
            str(Path.home() / r"AppData\Local\1Password\app\8\op_sdk_ipc_client.dll"),
        ]
    else:
        raise OSError(f"Unsupported operating system: {os_name}")

    for lib_path in locations:
        if os.path.exists(lib_path):
            return lib_path

    raise FileNotFoundError("1Password desktop application not found")


class DesktopCore:
    def __init__(self, account_name: str):
        # Determine the path to the desktop app.
        path = find_1password_lib_path()

        self.lib = ctypes.CDLL(path)
        self.account_name = account_name

        # Bind the Rust-exported functions
        self.send_message = self.lib.op_sdk_ipc_send_message
        self.send_message.argtypes = [
            POINTER(c_uint8),  # msg_ptr
            c_size_t,  # msg_len
            POINTER(POINTER(c_uint8)),  # out_buf
            POINTER(c_size_t),  # out_len
            POINTER(c_size_t),  # out_cap
        ]
        self.send_message.restype = c_int32

        self.free_message = self.lib.op_sdk_ipc_free_response
        self.free_message.argtypes = [POINTER(c_uint8), c_size_t, c_size_t]
        self.free_message.restype = None

    def call_shared_library(self, payload: str, operation_kind: str) -> bytes:
        # Prepare the input
        encoded_payload = base64.b64encode(payload.encode("utf-8")).decode("utf-8")
        data = {
            "kind": operation_kind,
            "account_name": self.account_name,
            "payload": encoded_payload,
        }
        message = json.dumps(data).encode("utf-8")

        # Prepare output parameters
        out_buf = POINTER(c_uint8)()
        out_len = c_size_t()
        out_cap = c_size_t()

        ret = self.send_message(
            (ctypes.cast(message, POINTER(c_uint8))),
            len(message),
            byref(out_buf),
            byref(out_len),
            byref(out_cap),
        )

        err = error_from_return_code(ret)
        if err is not None:
            raise err

        # Copy bytes into Python
        data = ctypes.string_at(out_buf, out_len.value)

        # Free memory via Rust's exported function
        self.free_message(out_buf, out_len, out_cap)

        parsed = json.loads(data)
        payload = bytes(parsed.get("payload", [])).decode("utf-8")

        success = parsed.get("success", False)
        if not success:
            e = Exception(payload)
            e.msg = payload
            raise_typed_exception(e)

        return payload

    async def init_client(self, config: dict) -> int:
        payload = json.dumps(config)
        resp = self.call_shared_library(payload, "init_client")
        return json.loads(resp)

    async def invoke(self, invoke_config: dict) -> str:
        payload = json.dumps(invoke_config)
        return self.call_shared_library(payload, "invoke")

    def release_client(self, client_id: int):
        payload = json.dumps(client_id)
        try:
            self.call_shared_library(payload, "release_client")
        except Exception as e:
            print(f"failed to release client: {e}")


ERR_CHANNEL_CLOSED = (
    "desktop app connection channel is closed. "
    "Make sure Settings > Developer > Integrate with other apps is enabled, "
    "or contact 1Password support"
)

ERR_CONNECTION_DROPPED = (
    "connection was unexpectedly dropped by the desktop app. "
    "Make sure the desktop app is running and Settings > Developer > "
    "Integrate with other apps is enabled, or contact 1Password support"
)

ERR_INTERNAL_FMT = (
    "an internal error occurred. Please contact 1Password support "
    "and mention the return code: {}"
)


def error_from_return_code(ret_code: int) -> Exception | None:
    if ret_code == 0:
        return None

    is_darwin = sys.platform == "darwin"

    if is_darwin:
        if ret_code == -3:
            return RuntimeError(ERR_CHANNEL_CLOSED)
        elif ret_code == -7:
            return RuntimeError(ERR_CONNECTION_DROPPED)
        else:
            return RuntimeError(ERR_INTERNAL_FMT.format(ret_code))
    else:
        if ret_code == -2:
            return RuntimeError(ERR_CHANNEL_CLOSED)
        elif ret_code == -5:
            return RuntimeError(ERR_CONNECTION_DROPPED)
        else:
            return RuntimeError(ERR_INTERNAL_FMT.format(ret_code))
