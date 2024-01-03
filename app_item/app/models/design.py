ifrom pydantic import BaseModel, ConfigDict
from uuid import UUID


class Design(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    image_url: str


class CreateDesignRequest(BaseModel):
    name: str
    image_url: str
