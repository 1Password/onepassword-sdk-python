#!/usr/bin/env python3
"""Verify the Rust internal build (unencrypted_cc_client_test + logging).

Requires:
  - OP_SERVICE_ACCOUNT_TOKEN set

The Rust [INFO] line only appears when the native library was built with the
'internal' Cargo feature. That build is done from the sdk-core repo:
  - macOS/Linux (with sdk-core): make local/python-internal

If you only have the onepassword-sdk-python repo (e.g. on Linux without sdk-core),
the shipped .so is built without 'internal', so you will see the Python messages
below but not the [INFO] line—that is expected. You can also add an internal-built
libop_uniffi_core.so (from sdk-core elsewhere) into src/onepassword/lib/<arch>/
and push it on your branch so pulls on Linux use that build.

Expected when internal build is active:
  [INFO] op_uniffi_core - Calling unencrypted cc client test: ...
"""
import asyncio
import importlib.util
import os
import platform
import sys

# Ensure stderr is visible and unbuffered (helps on Linux and macOS)
sys.stderr.reconfigure(line_buffering=True)


def _which_lib_path():
    """Report which arch dir is used and the exact native library path (same logic as core.UniffiCore)."""
    machine = platform.machine().lower()
    if machine in ["x86_64", "amd64"]:
        arch = "x86_64"
    elif machine in ["aarch64", "arm64"]:
        arch = "aarch64"
    else:
        return None, None, f"unsupported: {machine}"
    ext = "dylib" if sys.platform == "darwin" else "so"
    spec = importlib.util.find_spec(f"onepassword.lib.{arch}.op_uniffi_core")
    if not spec or not spec.origin:
        return arch, None, "module not found"
    lib_dir = os.path.dirname(spec.origin)
    lib_path = os.path.join(lib_dir, f"libop_uniffi_core.{ext}")
    return arch, lib_path, None


async def main():
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    if not token:
        print("Set OP_SERVICE_ACCOUNT_TOKEN and re-run.", file=sys.stderr)
        sys.exit(1)

    # Show which arch and path are used so you can confirm the right .so is loaded
    arch, lib_path, err = _which_lib_path()
    print(f"platform.machine() = {platform.machine()!r}  ->  using lib from: /{arch}/", file=sys.stderr)
    if lib_path:
        print(f"Native library path: {lib_path}", file=sys.stderr)
        print(f"File exists: {os.path.exists(lib_path)}", file=sys.stderr)
    if err:
        print(f"Note: {err}", file=sys.stderr)

    from onepassword import Client

    print("Calling Client.authenticate() (first call runs Rust init_logging_once + cc test)...", file=sys.stderr)
    sys.stderr.flush()
    client = await Client.authenticate(
        auth=token,
        integration_name="Verify Internal",
        integration_version="v1.0.0",
    )
    print(
        "Done. If you saw [INFO] op_uniffi_core above, the internal build is active. "
        "If not, the native lib was built without the internal feature (normal when you only have this repo).",
        file=sys.stderr,
    )

if __name__ == "__main__":
    asyncio.run(main())
