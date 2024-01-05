from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

class CreatePaymentRequest(BaseModel):
    sum: int
    receiver: str
    order_id: UUID
    user_id: UUID