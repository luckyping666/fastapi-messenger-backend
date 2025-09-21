from sqlalchemy.orm import Session
from app.models.chat_model import Chat
from sqlalchemy import or_, and_
from typing import Optional, List


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_chat_between_users(self, user1_id: int, user2_id: int) -> Optional[Chat]:
        return (
            self.db.query(Chat)
            .filter(
                or_(
                    and_(Chat.user1_id == user1_id, Chat.user2_id == user2_id),
                    and_(Chat.user1_id == user2_id, Chat.user2_id == user1_id),
                )
            )
            .first()
        )

    def create_chat(self, user1_id: int, user2_id: int) -> Chat:
        chat = Chat(user1_id=user1_id, user2_id=user2_id)
        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)
        return chat

    def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        return self.db.query(Chat).filter(Chat.id == chat_id).first()

    def get_user_chats(self, user_id: int) -> List[Chat]:
        return (
            self.db.query(Chat)
            .filter(or_(Chat.user1_id == user_id, Chat.user2_id == user_id))
            .all()
        )
