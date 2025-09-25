from pydantic import BaseModel
from datetime import datetime


class MessageCreateRequest(BaseModel):
    chat_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    content: str
    author_id: int  # <-- здесь мы будем использовать author_id из модели
    created_at: datetime
    is_read: bool

