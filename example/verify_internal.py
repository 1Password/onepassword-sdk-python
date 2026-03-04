#!/usr/bin/env python3
"""Verify the Rust internal build (unencrypted_cc_client_test + logging).

Requires:
  - OP_SERVICE_ACCOUNT_TOKEN set
  - SDK built from sdk-core on this machine:
      macOS: make local/python-internal
      Linux: make local/python-internal   (builds .so with internal feature)

You should see a line like:
  [INFO] op_uniffi_core - Calling unencrypted cc client test: ...
If you see nothing from Rust, the native lib was built without the 'internal' feature,
or you are running a copy of the SDK that was built on another OS (e.g. .dylib on Linux).
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
    print("Done. If you saw [INFO] op_uniffi_core above, the internal build is active.", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())
