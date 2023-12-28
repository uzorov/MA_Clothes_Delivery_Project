import enum
from uuid import UUID, uuid4
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Json


class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    price: float
    size: str
    count: int


class Cart(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = uuid4()
    items: List[dict]
    total: float

