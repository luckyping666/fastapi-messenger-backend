from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey, func
from db.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int]              = mapped_column(Integer, primary_key=True, index=True)
    chat_id: Mapped[int]         = mapped_column(Integer, ForeignKey("chats.id"), nullable=False)
    author_id: Mapped[int]       = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    content: Mapped[str]         = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_read: Mapped[bool]        = mapped_column(Boolean, default=False)

    # Связи
    chat: Mapped["Chat"]   = relationship("Chat", back_populates="messages") # type: ignore
    author: Mapped["User"] = relationship("User", back_populates="messages") # type: ignore
