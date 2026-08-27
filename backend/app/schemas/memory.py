from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MemoryBase(BaseModel):
    content: str


class MemoryCreate(MemoryBase):
    image_url: Optional[str] = None
    image_name: Optional[str] = None


class MemoryUpdate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None
    image_name: Optional[str] = None


class MemoryInDBBase(MemoryBase):
    id: int
    user_id: int
    vector_id: Optional[str] = None

    # Photo support
    image_url: Optional[str] = None
    image_name: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Memory(MemoryInDBBase):
    pass


class MemorySearch(BaseModel):
    query: str
    limit: int = 5