from src.db.database import engine

try:
    with engine.connect() as connection:
        print("✅ Підключення до бази успішне!")
except Exception as e:
    print("❌ Помилка підключення:", e)