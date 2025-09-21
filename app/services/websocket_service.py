from app.core.connection_manager import ConnectionManager
from app.services.message_service import MessageService
from app.models.user_model import User

class WebSocketService:
    def __init__(self, connection_manager: ConnectionManager, message_service: MessageService):
        self.manager = connection_manager
        self.message_service = message_service

    async def connect_user(self, chat_id: int, websocket):
        await self.manager.connect(chat_id, websocket)

    def disconnect_user(self, chat_id: int, websocket):
        self.manager.disconnect(chat_id, websocket)

    async def handle_message(self, chat_id: int, user: User, message: str):
        # Сохраняем сообщение в БД
        msg = self.message_service.send_message(chat_id, user.id, message)
        # Рассылаем всем подключённым к чату
        await self.manager.broadcast(chat_id, f"{user.username}: {msg.content}")
        return msg
