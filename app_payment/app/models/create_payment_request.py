from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

from app.models.payment_model import PaymentType


class CreatePaymentRequest(BaseModel):
    sum: int
    order_id: UUID
    user_id: UUID
    type: PaymentType