import enum
from uuid import UUID, uuid4
from typing import List
from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    price: float
    size: str
    count: int


class CartStatuses(enum.Enum):
    CREATED = 'CREATED'
    IN_ORDER = 'DONE'


class Cart(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = uuid4()
    user_id: UUID
    items: List[dict]
    total: float
    status: CartStatuses
