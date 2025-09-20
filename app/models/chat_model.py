from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, func
from app.db.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int]              = mapped_column(Integer, primary_key=True, index=True)
    user1_id: Mapped[int]        = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id: Mapped[int]        = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user1: Mapped["User"]             = relationship("User", foreign_keys=[user1_id], back_populates="chats_as_user1") # type: ignore
    user2: Mapped["User"]             = relationship("User", foreign_keys=[user2_id], back_populates="chats_as_user2") # type: ignore
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat") # type: ignore
