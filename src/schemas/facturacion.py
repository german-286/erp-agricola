from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from decimal import Decimal

# --- CLIENTE ---
class ClienteBase(BaseModel):
    nombre_empresa: str
    nif_cif: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    usuario_id: int
    model_config = ConfigDict(from_attributes=True)

# --- LÍNEA FACTURA ---
class LineaFacturaBase(BaseModel):
    concepto: str
    cantidad: Decimal
    precio_unitario: Decimal

class LineaFacturaCreate(LineaFacturaBase):
    pass

class LineaFacturaResponse(LineaFacturaBase):
    id: int
    factura_id: int
    subtotal: Decimal
    model_config = ConfigDict(from_attributes=True)

# --- FACTURA ---
class FacturaCreate(BaseModel):
    cliente_id: int
    numero_factura: str
    fecha_emision: date
    porcentaje_iva: Optional[Decimal] = Decimal("21.0")
    porcentaje_irpf: Optional[Decimal] = Decimal("0.0")
    lineas: List[LineaFacturaCreate]

class FacturaResponse(BaseModel):
    id: int
    usuario_id: int
    cliente_id: int
    numero_factura: str
    fecha_emision: date
    porcentaje_iva: Decimal
    porcentaje_irpf: Decimal
    total: Decimal
    lineas: List[LineaFacturaResponse] = []

    model_config = ConfigDict(from_attributes=True)
