from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict
from app.models.design import Design


class Item(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = uuid4()
    name: str
    price: float
    design: Design


class CreateItemRequest(BaseModel):
    id: UUID = uuid4()
