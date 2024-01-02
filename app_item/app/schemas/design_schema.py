from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base


class Design(Base):
    __tablename__ = 'designs'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)