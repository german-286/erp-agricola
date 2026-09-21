from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.db.session import get_db
from src.models.explotacion import DiarioOperaciones, CampanaParcela
from src.schemas.explotacion import DiarioOperacionesCreate, DiarioOperacionesResponse

router = APIRouter(prefix="/operaciones", tags=["Diario de Operaciones"])

@router.post("/", response_model=DiarioOperacionesResponse, status_code=status.HTTP_201_CREATED)
def registrar_operacion(operacion: DiarioOperacionesCreate, db: Session = Depends(get_db)):
    # Verificar que existe la relación campana_parcela
    cp = db.query(CampanaParcela).filter(CampanaParcela.id == operacion.campana_parcela_id).first()
    if not cp:
        raise HTTPException(
            status_code=404, 
            detail="La relación Campaña-Parcela especificada no existe."
        )

    nueva_operacion = DiarioOperaciones(
        campana_parcela_id=operacion.campana_parcela_id,
        fecha=operacion.fecha,
        tipo_operacion=operacion.tipo_operacion,
        producto_aplicado=operacion.producto_aplicado,
        coste_mano_obra=operacion.coste_mano_obra
    )
    
    db.add(nueva_operacion)
    db.commit()
    db.refresh(nueva_operacion)
    return nueva_operacion

@router.get("/campana-parcela/{campana_parcela_id}", response_model=List[DiarioOperacionesResponse])
def listar_operaciones_por_cultivo(campana_parcela_id: int, db: Session = Depends(get_db)):
    return db.query(DiarioOperaciones).filter(
        DiarioOperaciones.campana_parcela_id == campana_parcela_id
    ).all()
