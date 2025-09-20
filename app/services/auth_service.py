from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security.password_service import PasswordService
from app.core.security.token_service import TokenService
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.models.user_model import User


class AuthService:
    def __init__(
        self,
        db: Session,
        password_service: PasswordService,
        token_service: TokenService
    ):
        self.db = db
        self.password_service = password_service
        self.token_service = token_service
        self.user_repo = UserRepository(db)
        self.token_repo = TokenRepository(db)

    
    def register(self, email: str, username: str, password: str) -> User:
        if self.user_repo.get_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = self.password_service.hash_password(password)
        return self.user_repo.create(email=email, username=username, hashed_password=hashed_password)

    
    def login(self, email: str, password: str) -> dict:
        user = self.user_repo.get_by_email(email)
        if not user or not self.password_service.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = self.token_service.create_access_token({"sub": str(user.id)})
        refresh_token = self.token_service.create_refresh_token({"sub": str(user.id)})

        expires_at = datetime.utcnow() + timedelta(minutes=self.token_service.refresh_token_expire_minutes)
        self.token_repo.save_refresh_token(user.id, refresh_token, expires_at)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    
    def refresh_tokens(self, refresh_token: str) -> dict:
        payload = self.token_service.decode_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = int(payload.get("sub"))
        token_in_db = self.token_repo.get_active_token(user_id, refresh_token)
        if not token_in_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired or revoked"
            )

        # Деактивируем старый токен
        self.token_repo.deactivate_token(user_id, refresh_token)

        # Генерируем новые токены
        new_access_token = self.token_service.create_access_token({"sub": str(user_id)})
        new_refresh_token = self.token_service.create_refresh_token({"sub": str(user_id)})
        expires_at = datetime.utcnow() + timedelta(minutes=self.token_service.refresh_token_expire_minutes)
        self.token_repo.save_refresh_token(user_id, new_refresh_token, expires_at)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    
    def refresh_access_token(self, refresh_token: str) -> dict:
        payload = self.token_service.decode_token(refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = int(payload.get("sub"))
        token_in_db = self.token_repo.get_active_token(user_id, refresh_token)
        if not token_in_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired or revoked"
            )

        new_access_token = self.token_service.create_access_token({"sub": str(user_id)})
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    
    def logout(self, user_id: int, refresh_token: str) -> None:
        token_in_db = self.token_repo.get_active_token(user_id, refresh_token)
        if token_in_db:
            self.token_repo.deactivate_token(user_id, refresh_token)


    def logout_all_devices(self, user_id: int) -> None:
        self.token_repo.delete_all_tokens_for_user(user_id)
