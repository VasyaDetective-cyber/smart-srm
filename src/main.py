from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart CRM API!", "status": "ok"}