from sqlalchemy import Column, String, Enum, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=True)
    design = Column(JSON, nullable=True)
