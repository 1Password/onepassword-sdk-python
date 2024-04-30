from .core import _invoke

class Items:
  def __init__(self, client_id):
    self.client_id = client_id

  async def get(self, vault_id, item_id): 

   response = await _invoke({
		"clientId": self.client_id,
	   "invocation": {
			"name": "Get",
			"parameters": {  
			   "vault_id": vault_id, 
			   "item_id": item_id, 
			}
			}
		})

   return response


async def create(self, item): 

   response = await _invoke({
		"clientId": self.client_id,
	   "invocation": {
			"name": "Create",
			"parameters": {  
			   "item": item, 
			}
			}
		})

   return response


