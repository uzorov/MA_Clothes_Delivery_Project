
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class Payment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    order_id: UUID
    receiver: str
    sum: int

