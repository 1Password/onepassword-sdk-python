from onepassword.secrets import Secrets
import os

def test_resolve_secret_reference():
    print("Starting resolve_secret_reference test")
    test_secret_ref = os.getenv("CORE_SDK_TEST_SECRET_REF")
    if not test_secret_ref:
        raise ValueError("CORE_SDK_TEST_SECRET_REF must be set.")
    Secrets.validate_secret_reference(test_secret_ref)
    print("Finished resolve_secret_reference test successfully")

if __name__ == "__main__":
    test_resolve_secret_reference()
