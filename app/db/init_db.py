from app.db.db import engine
from app.db.base import Base 

def init_db():
    """
    Создаёт все таблицы в базе данных, если их ещё нет.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Все таблицы успешно созданы")

if __name__ == "__main__":
    init_db()
