from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.models.explotacion import Parcela
from src.models.usuario import Usuario
from src.schemas.explotacion import ParcelaCreate, ParcelaResponse

router = APIRouter(prefix="/parcelas", tags=["Parcelas & Fincas"])

@router.post("/usuario/{usuario_id}", response_model=ParcelaResponse, status_code=status.HTTP_201_CREATED)
def crear_parcela(usuario_id: int, parcela: ParcelaCreate, db: Session = Depends(get_db)):
    # Verificar que el usuario existe
    usr = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usr:
        raise HTTPException(status_code=44, detail="El usuario especificado no existe.")

    nueva_parcela = Parcela(
        usuario_id=usuario_id,
        nombre_finca=parcela.nombre_finca,
        poligono=parcela.poligono,
        parcela=parcela.parcela,
        recinto=parcela.recinto,
        referencia_catastral=parcela.referencia_catastral,
        superficie_ha=parcela.superficie_ha,
        regimen=parcela.regimen,
        coste_renta_campana=parcela.coste_renta_campana
    )
    
    db.add(nueva_parcela)
    db.commit()
    db.refresh(nueva_parcela)
    return nueva_parcela

@router.get("/usuario/{usuario_id}", response_model=List[ParcelaResponse])
def listar_parcelas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return db.query(Parcela).filter(Parcela.usuario_id == usuario_id).all()
