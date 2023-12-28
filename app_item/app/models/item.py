import enum
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, validator, HttpUrl
from pydantic.color import Color


class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = uuid4()
    name: str
    price: float

