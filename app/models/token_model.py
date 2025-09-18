from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Boolean, ForeignKey
from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int]              = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int]         = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token: Mapped[str]           = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool]      = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens") # type: ignore
