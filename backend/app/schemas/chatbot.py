from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    image_url: Optional[str] = None
    image_name: Optional[str] = None