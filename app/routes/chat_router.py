from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.core.dependencies import get_current_user
from app.services.chat_service import ChatService
from app.schemas.chat_schema import ChatResponse, ChatCreateRequest
from app.models.user_model import User


router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatResponse)
def create_chat(
    data: ChatCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    chat = service.get_or_create_chat(current_user.id, data.user2_id)
    return chat


@router.get("/", response_model=List[ChatResponse])
def get_user_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return service.get_user_chats(current_user.id)


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat_by_id(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    chat = service.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
