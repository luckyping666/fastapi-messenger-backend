from sqlalchemy.orm import Session
from app.models.chat_model import Chat
from app.models.message_model import Message
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
        chats = (
            self.db.query(Chat)
            .filter((Chat.user1_id == user_id) | (Chat.user2_id == user_id))
            .all()
        )

        result = []

        for chat in chats:
            last_msg = (
                self.db.query(Message)
                .filter(Message.chat_id == chat.id)
                .order_by(Message.created_at.desc())
                .first()
            )
            result.append(
                {
                    "id": chat.id,
                    "user1_id": chat.user1_id,
                    "user2_id": chat.user2_id,
                    "created_at": chat.created_at,
                    "last_message": last_msg.content if last_msg else "",
                }
            )

        return result