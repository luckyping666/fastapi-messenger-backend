from sqlalchemy.orm import Session
from app.models.message_model import Message
from typing import Optional, List


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, chat_id: int, sender_id: int, content: str) -> Message:
        message = Message(chat_id=chat_id, author_id=sender_id, content=content)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_by_chat(self, chat_id: int) -> List[Message]:
        return (
            self.db.query(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(Message.created_at.asc())
            .all()
        )

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        return self.db.query(Message).filter(Message.id == message_id).first()

    def delete_message(self, message_id: int) -> bool:
        message = self.get_message_by_id(message_id)
        if not message:
            return False
        self.db.delete(message)
        self.db.commit()
        return True
