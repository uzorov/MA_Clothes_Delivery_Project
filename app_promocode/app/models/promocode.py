from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict


class Promocode(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = uuid4()
    code: str
    discount: float
