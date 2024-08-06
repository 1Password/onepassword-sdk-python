import json
from pydantic import BaseModel, Field, ConfigDict, AliasGenerator
from typing import Annotated, List, Literal, Optional
from pydantic.alias_generators import to_camel

class Foo(BaseModel):
    model_config = ConfigDict(populate_by_name=True) 

    field_test: str = Field(alias="fieldTest")


if __name__ == "__main__":
    f = Foo(field_test="asfdf")

    x = f.model_dump_json(by_alias=True)
    print(x)

    y = Foo.model_validate_json(x)
    print(y)

