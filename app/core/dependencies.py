from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.core.security.password_service import PasswordService
from app.core.security.token_service import TokenService
from app.services.auth_service import AuthService


def get_password_service() -> PasswordService:
    return PasswordService()


def get_token_service() -> TokenService:
    return TokenService()


def get_auth_service(
    db: Session = Depends(get_db),
    password_service: PasswordService = Depends(get_password_service),
    token_service: TokenService = Depends(get_token_service),
) -> AuthService:
    return AuthService(db=db, password_service=password_service, token_service=token_service)
