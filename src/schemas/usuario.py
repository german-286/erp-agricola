from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- CLIENTE SCHEMAS ---
class ClienteBase(BaseModel):
    nif_cif: str
    nombre_empresa: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True

# --- USUARIO SCHEMAS ---
class UsuarioBase(BaseModel):
    nombre: str
    nif_cif: str
    email: EmailStr
    direccion_fiscal: Optional[str] = None
    iban: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
