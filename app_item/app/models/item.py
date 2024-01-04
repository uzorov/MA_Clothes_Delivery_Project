from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict


class Design(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    image_url: str


class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = uuid4()
    name: str
    price: float
    design: str


class CreateItemRequest(BaseModel):
    id: UUID = uuid4()
