# /app_delivery/models/delivery.py
from __future__ import annotations

import enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DeliveryStatuses(enum.Enum):
    CREATED = 'created'
    IN_PROCESS = 'in_process'
    DONE = 'done'
    CANCELED = 'canceled'


class DeliveryTypes(enum.Enum):
    PICKUP = 'pickup'
    DELIVERY = 'delivery'


class Delivery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    address: str
    date: datetime
    status: DeliveryStatuses
    type: DeliveryTypes


class CreateDeliveryRequest(BaseModel):
    id: UUID
