from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.models.explotacion import Campana, CampanaParcela, Parcela
from src.schemas.explotacion import (
    CampanaCreate, CampanaResponse, 
    CampanaParcelaCreate, CampanaParcelaResponse
)

router = APIRouter(prefix="/campanas", tags=["Campañas & Cultivos"])

@router.post("/", response_model=CampanaResponse, status_code=status.HTTP_201_CREATED)
def crear_campana(campana: CampanaCreate, db: Session = Depends(get_db)):
    nueva_campana = Campana(
        nombre=campana.nombre,
        fecha_inicio=campana.fecha_inicio,
        fecha_fin=campana.fecha_fin
    )
    db.add(nueva_campana)
    db.commit()
    db.refresh(nueva_campana)
    return nueva_campana

@router.get("/", response_model=List[CampanaResponse])
def listar_campanas(db: Session = Depends(get_db)):
    return db.query(Campana).all()

@router.post("/asignar-parcela", response_model=CampanaParcelaResponse, status_code=status.HTTP_201_CREATED)
def asignar_parcela_a_campana(datos: CampanaParcelaCreate, db: Session = Depends(get_db)):
    # Verificar que existen la campaña y la parcela
    camp = db.query(Campana).filter(Campana.id == datos.campana_id).first()
    if not camp:
        raise HTTPException(status_code=404, detail="La campaña especificada no existe.")
        
    parc = db.query(Parcela).filter(Parcela.id == datos.parcela_id).first()
    if not parc:
        raise HTTPException(status_code=404, detail="La parcela especificada no existe.")

    asignacion = CampanaParcela(
        campana_id=datos.campana_id,
        parcela_id=datos.parcela_id,
        tipo_cultivo=datos.tipo_cultivo,
        estado_cultivo=datos.estado_cultivo
    )
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)
    return asignacion
