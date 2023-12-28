from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

class CreateDesignRequest(BaseModel):
    name: str
    image_url: str