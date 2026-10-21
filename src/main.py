import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from src.core.config import settings
from src.api.routers import customer

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)
app.include_router(customer.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart CRM API!", "status": "ok"}