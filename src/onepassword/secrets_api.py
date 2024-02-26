from core import Invoke

# Secrets represents all operations the SDK client can perform on 1Password secrets.
class Secrets:
    def __init__(self, client_id):
        self.client_id = client_id

    async def resolve(self, reference):
        response = await Invoke({
            "clientId": self.client_id,
            "invocation": {
                "name": "Resolve",
                "parameters": reference,
                }
            })
        return response
