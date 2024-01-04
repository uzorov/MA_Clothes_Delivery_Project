from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from app.schemas.base_schema import Base

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True))
    order_id = Column(UUID(as_uuid=True))
    receiver = Column(String, nullable=False)
    sum = Column(Integer, nullable=False)
