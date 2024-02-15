from src.sdk import client as onepassword  # temporary example syntax, must be changed before release
import os

def main():
    # your 1Password service account token
    token = os.environ['OP_SERVICE_ACCOUNT_TOKEN']

    # initialize Client to connect to 1Password
    client = onepassword.Client(token, onepassword.DEFAULT_INTEGRATION_NAME, onepassword.DEFAULT_INTEGRATION_VERSION)

    # resolve secret reference
    result = client.secrets.resolve(reference="<your-secret-reference>")
    print(result)

if __name__ == '__main__':
    main()