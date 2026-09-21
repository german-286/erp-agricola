from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import date

# --- PARCELA SCHEMAS ---
class ParcelaBase(BaseModel):
    nombre_finca: str
    provincia: Optional[str] = "Granada"
    municipio: Optional[str] = "Granada"
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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)

# --- CAMPAÑA SCHEMAS ---
class CampanaBase(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class CampanaCreate(CampanaBase):
    pass

class CampanaResponse(CampanaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- CAMPAÑA PARCELA SCHEMAS ---
class CampanaParcelaBase(BaseModel):
    tipo_cultivo: str
    estado_cultivo: Optional[str] = "EN_PRODUCCION"

class CampanaParcelaCreate(CampanaParcelaBase):
    campana_id: int
    parcela_id: int

class CampanaParcelaResponse(CampanaParcelaBase):
    id: int
    campana_id: int
    parcela_id: int

    model_config = ConfigDict(from_attributes=True)
