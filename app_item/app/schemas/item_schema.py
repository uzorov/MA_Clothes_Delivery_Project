from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.models.design_model import Design

from app.schemas.base_schema import Base


class Design(Base):
    __tablename__ = 'designs'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Enum, nullable=True)
    design = Column(Design, nullable=True)
