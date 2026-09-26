from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal

class MarketplaceServicioBase(BaseModel):
    titulo: str
    categoria: str
    empresa_nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_estimado: Optional[Decimal] = None
    unidad_precio: Optional[str] = None
    provincia: Optional[str] = None
    telefono: Optional[str] = None
    es_patrocinado: Optional[bool] = False

class MarketplaceServicioCreate(MarketplaceServicioBase):
    pass

class MarketplaceServicioResponse(MarketplaceServicioBase):
    id: int
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)
