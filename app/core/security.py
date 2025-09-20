from passlib.context import CryptContext


class PasswordService:
    """
    Сервис для работы с паролями.
    Использует bcrypt через passlib.
    """

    def __init__(self) -> None:
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """
        Вернуть bcrypt-хэш пароля.
        """
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверить пароль.
        """
        return self._pwd_context.verify(plain_password, hashed_password)

