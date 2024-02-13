from core import Invoke
import os

token = os.environ['OP_SERVICE_ACCOUNT_TOKEN']


# SecretsAPI represents all operations the SDK client can perform on 1Password secrets.
class SecretsApi:
    def Resolve(self, reference):
        response = Invoke({
            "clientId": self.client_id,
            "invocation": {
                "name": "Resolve",
                "parameters": reference,
                }
            })
        return response


class SecretsSource:
    def __init__(self, client_id, core):
        self.clientID = client_id
        self.core = core
