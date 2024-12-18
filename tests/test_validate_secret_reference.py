from onepassword.secrets import Secrets

# Validate secret reference to ensure no syntax errors
def test_validate_secret_reference():
    print("Starting validate_secret_reference test")
    Secrets.validate_secret_reference("op://vault/item/field")
    print("Finished validate_secret_reference test successfully")

if __name__ == "__main__":
    test_validate_secret_reference()
