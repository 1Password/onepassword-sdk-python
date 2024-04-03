---
sidebar_label: secrets_api
title: onepassword.secrets_api
---

## Secrets Objects

```python
class Secrets()
```

Secrets represents all operations the SDK client can perform on 1Password secrets.

#### resolve

```python
async def resolve(reference)
```

resolve returns the secret the provided reference points to.

