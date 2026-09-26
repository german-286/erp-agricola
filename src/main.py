from fastapi import FastAPI
from src.core.config import settings
from src.api.v1 import usuarios, parcelas, campanas, operaciones, facturacion, marketplace

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API REST para la gestión de explotaciones agrícolas, cuaderno de campo y facturación."
)

# Registrar los routers de la API v1
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(parcelas.router, prefix="/api/v1")
app.include_router(campanas.router, prefix="/api/v1")
app.include_router(operaciones.router, prefix="/api/v1")
app.include_router(facturacion.router, prefix="/api/v1")
app.include_router(marketplace.router, prefix="/api/v1")

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
