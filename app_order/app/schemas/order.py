# /app/schemas/delivery.py

from sqlalchemy import Column, String, Integer, Enum, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship

from app.schemas.base_schema import Base
from app.models.order import OrderStatuses


class Order(Base):
    __tablename__ = 'orders'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    user_id = Column(UUID(as_uuid=True))
    status = Column(Enum(OrderStatuses), nullable=True)
    discount = Column(Float, nullable=True)
    price = Column(Float, nullable=True, default=1)
    cart = Column(UUID(as_uuid=True))