import datetime

from pydantic import BaseModel, ConfigDict


class AdBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    price: float
    author: str | None = None


class AdCreate(AdBase):
    pass

class AdUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None

class AdResponse(AdBase):
    id: int
    created_at: datetime.datetime
