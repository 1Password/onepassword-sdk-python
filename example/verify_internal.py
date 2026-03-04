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
import os
import sys

# Ensure stderr is visible and unbuffered (helps on Linux and macOS)
sys.stderr.reconfigure(line_buffering=True)

async def main():
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN")
    if not token:
        print("Set OP_SERVICE_ACCOUNT_TOKEN and re-run.", file=sys.stderr)
        sys.exit(1)

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
