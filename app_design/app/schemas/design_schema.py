from sqlalchemy import Column, String, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.design_model import DesignStatuses
from app.schemas.base_schema import Base


class Design(Base):
    __tablename__ = 'designs'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    status = Column(Enum(DesignStatuses), nullable=False)