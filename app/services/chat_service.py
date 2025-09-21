from sqlalchemy.orm import Session
from app.repositories.chat_repository import ChatRepository
from app.models.chat_model import Chat
from typing import List, Optional


class ChatService:
    def __init__(self, db: Session):
        self.chat_repo = ChatRepository(db)

    def get_or_create_chat(self, user1_id: int, user2_id: int) -> Chat:
        chat = self.chat_repo.get_chat_between_users(user1_id, user2_id)
        if chat:
            return chat
        return self.chat_repo.create_chat(user1_id, user2_id)

    def get_user_chats(self, user_id: int) -> List[Chat]:
        return self.chat_repo.get_user_chats(user_id)

    def get_chat_by_id(self, chat_id: int) -> Optional[Chat]:
        return self.chat_repo.get_chat_by_id(chat_id)
