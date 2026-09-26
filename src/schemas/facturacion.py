from pydantic import BaseModel, ConfigDict
from typing import Optional

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
