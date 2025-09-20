import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError
from app.core.config import settings


class TokenService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: Dict, expires_minutes: Optional[int] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=expires_minutes or self.access_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: Dict, expires_minutes: Optional[int] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=expires_minutes or self.refresh_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[Dict]:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            return None

    def hash_refresh_token(self, token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()
