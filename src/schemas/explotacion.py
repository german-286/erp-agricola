from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

# --- PARCELA SCHEMAS ---
class ParcelaBase(BaseModel):
    nombre_finca: str
    poligono: Optional[int] = None
    parcela: Optional[int] = None
    recinto: Optional[int] = None
    referencia_catastral: Optional[str] = None
    superficie_ha: Decimal
    regimen: Optional[str] = "PROPIEDAD"
    coste_renta_campana: Optional[Decimal] = Decimal("0.00")

class ParcelaCreate(ParcelaBase):
    pass

class ParcelaResponse(ParcelaBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True

# --- DIARIO DE OPERACIONES SCHEMAS ---
class DiarioOperacionesBase(BaseModel):
    fecha: date
    tipo_operacion: str
    producto_aplicado: Optional[str] = None
    coste_mano_obra: Optional[Decimal] = Decimal("0.00")

class DiarioOperacionesCreate(DiarioOperacionesBase):
    campana_parcela_id: int

class DiarioOperacionesResponse(DiarioOperacionesBase):
    id: int
    campana_parcela_id: int

    class Config:
        from_attributes = True
