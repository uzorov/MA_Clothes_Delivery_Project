from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class DesignStatuses(Enum):
    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'

class Design(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    image_url: str
    status: DesignStatuses

