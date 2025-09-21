from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.core.connection_manager import ConnectionManager
from app.services.message_service import MessageService
from app.services.websocket_service import WebSocketService
from app.models.user_model import User
from jose import jwt, JWTError
from fastapi import HTTPException
from app.core.config import settings
from app.repositories.user_repository import UserRepository

router = APIRouter()
manager = ConnectionManager()


# JWT validation for WebSocket
async def get_current_user_ws(token: str = Query(...), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


# WebSocket endpoint
@router.websocket("/ws/chat/{chat_id}")
async def chat_ws(
    websocket: WebSocket,
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_ws),
):
    ws_service = WebSocketService(manager, MessageService(db))

    await ws_service.connect_user(chat_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await ws_service.handle_message(chat_id, current_user, data)
    except WebSocketDisconnect:
        ws_service.disconnect_user(chat_id, websocket)
    except Exception:
        ws_service.disconnect_user(chat_id, websocket)
