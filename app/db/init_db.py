from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.user_model import User
from app.models.token_model import RefreshToken
from app.models.chat_model import Chat
from app.models.token_model import RefreshToken
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # показывает все SQL-запросы в консоли, удобно для отладки
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Все таблицы успешно созданы")

if __name__ == "__main__":
    init_db()
