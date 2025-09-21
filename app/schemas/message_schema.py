from pydantic import BaseModel
from datetime import datetime


class MessageCreateRequest(BaseModel):
    chat_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
