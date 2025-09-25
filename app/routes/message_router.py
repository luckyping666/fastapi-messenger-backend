from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.db import get_db
from app.core.dependencies import get_current_user
from app.services.message_service import MessageService
from app.schemas.message_schema import MessageResponse, MessageCreateRequest
from app.models.user_model import User


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/send", response_model=MessageResponse)
def send_message(
    data: MessageCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print('Папали')
    service = MessageService(db)
    return service.send_message(data.chat_id, current_user.id, data.content)


@router.get("/chat/{chat_id}", response_model=List[MessageResponse])
def get_chat_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MessageService(db)
    return service.get_chat_messages(chat_id)


@router.get("/{message_id}", response_model=MessageResponse)
def get_message_by_id(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MessageService(db)
    message = service.get_message_by_id(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = MessageService(db)
    success = service.delete_message(message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"detail": "Message deleted"}
