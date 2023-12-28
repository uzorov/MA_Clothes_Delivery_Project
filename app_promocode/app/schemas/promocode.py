from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base


class Promocode(Base):
    __tablename__ = 'promocodes'

    id = Column(UUID(as_uuid=True), primary_key=True)
    code = Column(Enum, nullable=False)
    discount = Column(Enum, nullable=False)
