from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, func
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int]                     = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str]               = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str]                  = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str]        = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool]             = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime]        = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_login: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship("RefreshToken", back_populates="user") # type: ignore
    chats_as_user1: Mapped[list["Chat"]]         = relationship("Chat", back_populates="user1", foreign_keys="[Chat.user1_id]") # type: ignore
    chats_as_user2: Mapped[list["Chat"]]         = relationship("Chat", back_populates="user2", foreign_keys="[Chat.user2_id]") # type: ignore
    messages: Mapped[list["Message"]]            = relationship("Message", back_populates="author") # type: ignore
