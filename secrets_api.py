from core import Invoke

# just putting this here for now
token = "ops_eyJzaWduSW5BZGRyZXNzIjoic2FtLTFwYXNzLWFsaWFzLmI1dGVzdC5jb20iLCJ1c2VyQXV0aCI6eyJtZXRob2QiOiJTUlBnLTQwOTYiLCJhbGciOiJQQkVTMmctSFMyNTYiLCJpdGVyYXRpb25zIjo2NTAwMDAsInNhbHQiOiIwMHBMNFJpUnRmazFLMm5RZWp3MUZnIn0sImVtYWlsIjoiZG93ajRrd3dndXJ3Z0AxcGFzc3dvcmRzZXJ2aWNlYWNjb3VudHMuY29tIiwic3JwWCI6IjI3YmM3MzI2NDY0NWNmMjUyZDg3ODEyNDc4MDY2MzA2OWYyNTkyY2Q0MDZhYjA3YTg3NWE1NjlmODEwOGYyZTkiLCJtdWsiOnsiYWxnIjoiQTI1NkdDTSIsImV4dCI6dHJ1ZSwiayI6IlJoVUhIaVBzT3JMWHdYOUctUXZ4ZDhTUTdKdmV1UGpuM25JWFREQTZ4MTQiLCJrZXlfb3BzIjpbImVuY3J5cHQiLCJkZWNyeXB0Il0sImt0eSI6Im9jdCIsImtpZCI6Im1wIn0sInNlY3JldEtleSI6IkEzLTJYQ1JDRy1KS05FTjUtU0I3UE0tQlk2QjktUkFHSEctOEpIWjQiLCJ0aHJvdHRsZVNlY3JldCI6eyJzZWVkIjoiMmE5ZDRjNjQ5NzMyMDhjNjgwZWU3ZjA2YmE2OTE3MzkxMzBkMDc4YjI2MTM1ZGIwYWRjNThkZjdlNTIyYmY2NyIsInV1aWQiOiJTM1NWUzVINDRGQVlOSzJUNzVKQ0pEWU5aWSJ9LCJkZXZpY2VVdWlkIjoidm94bHhnNGdlNHVkZzIyZ3RpbnlrajIyeTQifQ"

# SecretsAPI represents all operations the SDK client can perform on 1Password secrets.
class SecretsApi:
    def Resolve(reference):
        pass

# Note: this would be populated by createClient() in Go, which we are no longer using in Python
# the cliend_id in Resolve() can be defined multiple ways, such as a global variable, dictionary, singleton, parameter, etc. tbd which is the best
class SecretsSource:
    def __init__(self, clientID, core):
        self.clientID = clientID
        self.core = core

def Resolve(reference):
    client_id = 0 # satisfying the interpreter temporarily
    response = Invoke(dict(
		clientId = client_id, 
        invocation = dict(
            name = "Resolve",
            parameters = reference)
    ))
    return response

SecretsApi.Resolve = Resolve