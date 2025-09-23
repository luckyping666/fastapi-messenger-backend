from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatCreateRequest(BaseModel):
    user2_id: int  


class ChatResponse(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime
    last_message: Optional[str] = None

