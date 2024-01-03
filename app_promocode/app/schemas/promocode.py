from sqlalchemy import Column, Enum, String, Float
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base


class Promocode(Base):
    __tablename__ = 'promocodes'

    id = Column(UUID(as_uuid=True), primary_key=True)
    code = Column(String, nullable=False)
    discount = Column(Float, nullable=False)
