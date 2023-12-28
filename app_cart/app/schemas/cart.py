from sqlalchemy import Column, String, Float, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship

from app.schemas.base_schema import Base

class Cart(Base):
    __tablename__ = 'carts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    total = Column(Float, nullable=True, default=1)
    items = Column(JSON, nullable=True)