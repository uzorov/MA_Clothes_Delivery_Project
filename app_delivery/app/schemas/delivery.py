# /app/schemas/delivery.py

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base
from app.models.delivery import DeliveryStatuses
from app.models.delivery import DeliveryTypes


class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(UUID(as_uuid=True), primary_key=True)
    address = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    status = Column(Enum(DeliveryStatuses), nullable=False)
    type = Column(Enum(DeliveryTypes), nullable=False)
