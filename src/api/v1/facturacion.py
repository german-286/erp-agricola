from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.models.facturacion import Cliente
from src.schemas.facturacion import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/facturacion", tags=["Facturación & Clientes"])

@router.post("/clientes/usuario/{usuario_id}", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def crear_cliente(usuario_id: int, cliente: ClienteCreate, db: Session = Depends(get_db)):
    nuevo_cliente = Cliente(
        usuario_id=usuario_id,
        nombre_empresa=cliente.nombre_empresa,
        nif_cif=cliente.nif_cif,
        direccion=cliente.direccion,
        telefono=cliente.telefono,
        email=cliente.email
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@router.get("/clientes/usuario/{usuario_id}", response_model=List[ClienteResponse])
def listar_clientes_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Cliente).filter(Cliente.usuario_id == usuario_id).all()
