# /app_printing/schemas/printing.py

from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.schemas.base_schema import Base
from app.models.printing import PrintingStatuses


class Printing(Base):
    __tablename__ = 'printings'

    id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(DateTime, nullable=False)
    status = Column(Enum(PrintingStatuses), nullable=False)
