from datetime import datetime
from sqlalchemy.orm import Session
from app.models.token_model import RefreshToken


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_refresh_token(self, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_active=True
        )
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_active_token(self, user_id: int, token: str) -> RefreshToken | None:
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.token == token,
                RefreshToken.is_active == True,
                RefreshToken.expires_at > datetime.utcnow()
            )
            .first()
        )

    def deactivate_token(self, user_id: int, token: str) -> None:
        refresh_token = (
            self.db.query(RefreshToken)
            .filter(RefreshToken.user_id == user_id, RefreshToken.token == token)
            .first()
        )
        if refresh_token:
            refresh_token.is_active = False
            self.db.commit()

    def delete_all_tokens_for_user(self, user_id: int) -> None:
        self.db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
        self.db.commit()
