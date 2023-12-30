from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class PaymentType(Enum):
    PC = 'Кошелек ЮMoney'
    AC = 'Банковская карта'

class Payment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    receiver: str
    sum: int
    type: PaymentType

