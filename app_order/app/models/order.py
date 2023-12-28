import enum
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, validator


class OrderStatuses(enum.Enum):
    CREATED = 'created'
    PAID = 'paid'
    DONE = 'done'

class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID
    id: UUID = uuid4()
    cart: UUID
    status: OrderStatuses
    discount: float | None
    price: float
