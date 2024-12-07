
from onepassword.secrets import Secrets

# Validate secret reference to ensure no syntax errors
def validate_secret_reference():
    try:
        Secrets.validate_secret_reference("op://vault/item/field")
        print("Secret reference is of valid syntax")
    except Exception as error:
        print(error)

if __name__ == "__main__":
    validate_secret_reference()