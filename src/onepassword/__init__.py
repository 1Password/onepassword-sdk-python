# AUTO-GENERATED
from .client import Client
from .defaults import DEFAULT_INTEGRATION_NAME, DEFAULT_INTEGRATION_VERSION
from .types import * # noqa F403
from .secrets import Secrets
from .items import Items

import sys, inspect, typing

__all__ = [
    "Client",
    "Secrets",
    "Items",
    "DEFAULT_INTEGRATION_NAME",
    "DEFAULT_INTEGRATION_VERSION",
]

for name, obj in inspect.getmembers(sys.modules["onepassword.types"]):
    if inspect.isclass(obj) or type(eval(name)) == typing._LiteralGenericAlias:
        __all__.append(name)
