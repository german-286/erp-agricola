from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API REST para la gestión de explotaciones agrícolas, cuaderno de campo y facturación."
)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API del ERP Agrícola",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }
