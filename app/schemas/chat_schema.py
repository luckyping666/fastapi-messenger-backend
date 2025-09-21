from pydantic import BaseModel
from datetime import datetime


class ChatCreateRequest(BaseModel):
    user2_id: int  


class ChatResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime

    class Config:
        from_attributes = True 

