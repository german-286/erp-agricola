from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.models.usuario import Usuario
from src.schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Comprobar si el email o NIF ya existe
    usuario_existente = db.query(Usuario).filter(
        (Usuario.email == usuario.email) | (Usuario.nif_cif == usuario.nif_cif)
    ).first()
    
    if usuario_existente:
        raise HTTPException(
            status_code=400, 
            detail="Ya existe un usuario registrado con ese email o NIF/CIF."
        )

    # Crear el nuevo usuario (en producción la contraseña iría hasheada con passlib/bcrypt)
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        nif_cif=usuario.nif_cif,
        email=usuario.email,
        password_hash=usuario.password,  # Temporal sin hash para la prueba
        direccion_fiscal=usuario.direccion_fiscal,
        iban=usuario.iban
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Usuario).offset(skip).limit(limit).all()
