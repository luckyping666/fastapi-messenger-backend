from sqlalchemy.orm import Session
from repositories.message_repository import MessageRepository
from app.models.message_model import Message
from typing import List, Optional


class MessageService:
    def __init__(self, db: Session):
        self.message_repo = MessageRepository(db)

    def send_message(self, chat_id: int, sender_id: int, content: str) -> Message:
        return self.message_repo.create_message(chat_id, sender_id, content)

    def get_chat_messages(self, chat_id: int) -> List[Message]:
        return self.message_repo.get_messages_by_chat(chat_id)

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        return self.message_repo.get_message_by_id(message_id)

    def delete_message(self, message_id: int) -> bool:
        return self.message_repo.delete_message(message_id)
