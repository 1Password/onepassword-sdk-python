---
sidebar_label: client
title: onepassword.client
---

#### SDK\_VERSION

v0.1.0

## Client Objects

```python
class Client()
```

A client

#### authenticate

```python
@classmethod
async def authenticate(cls, auth, integration_name, integration_version)
```

authenticate returns an authenticated client or errors if any provided information, including the SA token, is incorrect
`integration_name` represents the name of your application and `integration_version` represents the version of your application.

#### new\_default\_config

```python
def new_default_config(auth, integration_name, integration_version)
```

Generates a configuration dictionary with the user&#x27;s parameters

