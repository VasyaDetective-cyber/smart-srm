
from sqlalchemy import text
from src.db.database import engine

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("✅ Підключення до бази успішне!")

except Exception as e:
    print(f"❌ Помилка підключення: {e}")

finally:
    engine.dispose()
